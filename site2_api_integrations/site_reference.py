from flask import Flask, render_template, request, g, session
from dotenv import load_dotenv
import os
from datetime import datetime
from logging_config import setup_logging  # Import the logging configuration
import inspect


# see routes/__init__.py
from routes import register_routes

# schwab-py import statement
from schwab import auth

# used to create the OAuth session
from services.login import createClientFromCallback

# Load environment variables from a custom file
load_dotenv('sitevars.prod.env')

# create the Flask app
app = Flask(__name__, template_folder="templates")

# Set up logging
setup_logging(app)

# Register all website routes (blueprints)
register_routes(app)

# The line app.secret_key = 'your_secret_key' is necessary for using Flask's session feature, which securely stores data across multiple requests. 
# Flask’s session object keeps data on the client-side but encrypts it before sending it to the client’s browser. 
# This encryption requires a secret key to sign and secure the data, ensuring that no one can tamper with it. Without a secret_key, 
# Flask won’t be able to safely encrypt or decrypt the session data.
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# Tells the server to monitor the sourcecode for changes to any HTML templates and reload
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Because we are building a reference design, implement this approach for which is the base template
#app.config['BASE_TEMPLATE'] = 'base.html'
app.config['BASE_TEMPLATE'] = 'base_reference.html'


# Log every request
@app.before_request
def log_request():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"---- {current_time} ---------------------------------------------")
    getEnv()
    print(f"Request: {request.method} {request.url}")
    print(f"Headers: {request.headers}")
    print(f"Body: {request.get_data()}")
    print(f"WORKER PID: {os.getpid()}")
    # retrieve the auth_context_state from the session, which was created on login (kinda)
    auth_context_state = session.get('auth_context_state')
    print(f"AUTH_CONTEXT_STATE: {auth_context_state}")
    print("ENVIRONMENT:")
    printEnv()
    print(f"^^^^ {current_time} ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    #
    # Additonal functionality checks
    #
    # set the base template to use for site navigation
    g.base_template = app.config['BASE_TEMPLATE']

    # DEVELOPER NOTES: We can set a new auth_context.state *** EXCEPT FOR *** the
    # workflow where we are being called back to the provider.  IF we set another
    # new auth_context.state on that request, then it will override the one we
    # already set and we have a CSRF token mismatch when attempting to retrieve
    # the bearer token.

    # authorization_url is used to drive navigation header for login/logout link depending if user is or is not logged in
    
    # Check if this is the OAuth callback request
    if request.path == '/' and 'session' in request.args:
        print(f"LOG REQUEST [ -------------------------- ][ We are being called back by the provider ]")
        # We blank out the authorization_url so the navigation header works properly after login
        g.authorization_url = ""
    else:
        print(f"LOG REQUEST [ -------------------------- ][ We are NOT being called back by the provider ]")

        # Token file is going to exist when a logout request hits the server.
        # BUT we need to create a new one for the user, to allow them to immediately
        # log back in, after clicking 'logout'

        if isLoggedInToSchwab() and request.path != '/logout':
            print(f"LOG REQUEST [ -------------------------- ][ YES WE ARE LOGGED IN (token file exists) ]")
            # This is logic error, fix.
            g.authorization_url = ""
        else:
            print(f"LOG REQUEST [ -------------------------- ][ CREATE NEW auth_context ]")
            # get an authorization context, which includes a 'state'.  This is part of handling a CSRF token which
            # maintains a single 'state' for authorizing.  Understanding CSRF tokens is beyond the scope of this application.
            api_key = g.client_id

            auth_context = auth.get_auth_context(api_key, g.redirect_uri)   

            # store the auth_context_state for future use in the login process
            # Store in a session instead of g, to persist over subsequent requests
            session['auth_context_state'] = auth_context.state

            print(f"SET NEW CONTEXT STATE: {auth_context.state}")

            # Should look like:
            #
            #  https://api.schwabapi.com/v1/oauth/authorize?response_type=code&client_id=REDACTED&redirect_uri=https%3A%2F%2Fwww.yourdomain.com&state=valueofCSRFtoken
            #
            g.authorization_url = auth_context.authorization_url
            


# ###################### MAIN ###########################
# Home route
@app.route('/')
def home():
    # Check for GET parameters 'code' and 'session'
    g.oauth_code = request.args.get('code')
    g.oauth_session = request.args.get('session')

    # DEV NOTE ? retry here ???
 
    # If oauth_code is set, this means the OAuth provider is calling this webpage back.  Get the bearerToken next.
    if g.oauth_code:
        print(f"MAIN [ -------------------------- ][ We are being called back by the provider ]")

        # Capture full URL
        received_url = request.url        

        print(f"Scraped oauth_code {g.oauth_code}")

        # NOTE: The process of calling this function finalizes the creation of the token
        #       file on the server (or localhost) so that 
        #       it can be used in subsequent future calls to schwab's API
        #
        try:
            client = createClientFromCallback(received_url)  # Call the function to get the bearer token    
            if client is None:
                print(f"MAIN [ no client returned ]")
            else:
                print(f"MAIN [ successfully got a client ]")
        except Exception as err:
            print(f"MAIN [ there was an exception while creating client: {err} ]")

    '''
    ORIGINAL Code inception - single use case whereby this *** only works ***
             for when a user is navigated to the home route ('/') and clicks "login"
             IF the user is on any other page and clicks on the login link, then
             there is a break in the workflow of this implementation design.

    # Check to see if a token file exists.  
    # If so, assume the user has logged in successfully and provide a logout link
    # If not, assume the user needs to login and provide a login link
    if g.token_path:
        if os.path.exists(g.token_path):
            # USER IS LOGGED IN
            g.authorization_url = ""

            print(f"USER IS LOGGED IN")
        else:
            # USER IS NOT LOGGED IN
            print(f"USER IS NOT LOGGED IN")
            # get an authorization context, which includes a 'state'.  This is part of handling a CSRF token which
            # maintains a single 'state' for authorizing.  Understanding CSRF tokens is beyond the scope of this application.
            api_key = g.client_id

            auth_context = auth.get_auth_context(api_key, g.redirect_uri)   

            # store the auth_context_state for future use in the login process
            # Store in a session instead of g, to persist over subsequent requests
            session['auth_context_state'] = auth_context.state

            print(f"SET NEW CONTEXT STATE: {auth_context.state}")

            # Should look like:
            #
            #  https://api.schwabapi.com/v1/oauth/authorize?response_type=code&client_id=REDACTED&redirect_uri=https%3A%2F%2Fwww.yourdomain.com&state=valueofCSRFtoken
            #
            g.authorization_url = auth_context.authorization_url
            print(f"MAIN [ authorization_url = {g.authorization_url} ]")
    '''

    

    # We use the authorization_url from the auth_context so that it can use the 'state' which is the CSRF token value for the session
    return render_template('home.html', base_template=g.base_template, title="Home", redirect_uri=g.redirect_uri, login_link_url=g.authorization_url)


def isLoggedInToSchwab():
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    # If we do not have any client_id set assume user is not logged in
    if not g.client_id:
        print(f"{ex_path} client_id is not set")
        return False

    # If we do not have any redirect_uri set assume user is not logged in
    if not g.redirect_uri:
        print(f"{ex_path} redirect_uri is not set")
        return False

    # If we do not have any token_path set assume user is not logged in
    if not g.token_path:
        print(f"{ex_path} token_path is not set")
        return False

    # If there is a token file which exists assume 
    # session is valid and the user is logged in
    print(f"{ex_path} token_path = {g.token_path}")
    if os.path.exists(g.token_path):
        print(f"{ex_path} TOKEN FILE EXISTS")
        return True
    else:
        print(f"{ex_path} NO TOKEN FILE ON SERVER")
        return False

# Function to print the environment variable value
def printEnv():
    print(f"[printEnv] Environment Variable client_id: {g.client_id}")
    print(f"[printEnv] Environment Variable client_secret: {g.client_secret}")
    print(f"[printEnv] Environment Variable consumer_key: {g.consumer_key}")
    print(f"[printEnv] Environment Variable redirect_url: {g.redirect_uri}")
    print(f"[printEnv] Environment Variable token_path: {g.token_path}")

# Function to get the environment variable value
def getEnv():
    # Secrets (stored in the dotenv file) are stored in 'g' (global variables) for use during API calls (see 'services')
    g.client_id = os.getenv('OAUTH_CLIENT_ID', 'Not set')
    g.client_secret = os.getenv('OAUTH_CLIENT_SECRET', 'Not set')
    g.consumer_key = os.getenv('OAUTH_CONSUMER_KEY', 'Not set')
    g.redirect_uri = os.getenv('REDIRECT_URI', 'Not set')
    g.token_path = os.getenv('TOKEN_PATH', 'Not set')

if __name__ == '__main__':
    # bind to localhost only
    host = "127.0.0.1"

    # bind to all interfaces
    host = "0.0.0.0"

    port = 5001
    app.run(host=host, port=port, debug=True)
