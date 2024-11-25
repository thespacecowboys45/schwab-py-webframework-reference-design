from flask import Flask, render_template, request, g, session
from dotenv import load_dotenv
import os
from datetime import datetime
from logging_config import setup_logging  # Import the logging configuration

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
    # set the base template to use with 'g'
    g.base_template = app.config['BASE_TEMPLATE']

    getEnv()
    worker_pid = os.getpid()
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"---- {current_time} ---------------------------------------------")
    print(f"Request: {request.method} {request.url}")
    print(f"Headers: {request.headers}")
    print(f"Body: {request.get_data()}")
    print(f"WORKER PID: {worker_pid}")
    print("ENVIRONMENT:")
    printEnv()
    print(f"^^^^ {current_time} ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")


# ###################### MAIN ###########################
# Home route
@app.route('/')
def home():
    # Check for GET parameters 'code' and 'session'
    g.oauth_code = request.args.get('code')
    g.oauth_session = request.args.get('session')
 
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
        client = createClientFromCallback(received_url)  # Call the function to get the bearer token    
        if client is None:
            print(f"MAIN [ no client returned ]")
        else:
            print(f"MAIN [ successfully got a client ]")

    # Check to see if a token file exists.  
    # If so, assume the user has logged in successfully and provide a logout link
    # If not, assume the user needs to login and provide a login link
    if g.token_path:
        if os.path.exists(g.token_path):
            # USER IS LOGGED IN
            authorization_url = ""

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

            # Should look like:
            #
            #  https://api.schwabapi.com/v1/oauth/authorize?response_type=code&client_id=REDACTED&redirect_uri=https%3A%2F%2Fwww.yourdomain.com&state=valueofCSRFtoken
            #
            authorization_url = auth_context.authorization_url
            print(f"MAIN [ authorization_url = {authorization_url} ]")

    # We use the authorization_url from the auth_context so that it can use the 'state' which is the CSRF token value for the session
    return render_template('home.html', base_template=g.base_template, title="Home", redirect_uri=g.redirect_uri, login_link_url=authorization_url)

# Function to print the environment variable value
def printEnv():
    print(f"[printEnv] Environment Variable client_id: {g.client_id}")
    print(f"[printEnv] Environment Variable client_secret: {g.client_secret}")
    print(f"[printEnv] Environment Variable consumer_key: {g.consumer_key}")
    print(f"[printEnv] Environment Variable redirect_url: {g.redirect_uri}")
    print(f"[printEnv] Environment Variable token_path: {g.token_path}")

# Function to get the environment variable value
def getEnv():
    # Secrets (uses the dotenv file)
    g.client_id = os.getenv('OAUTH_CLIENT_ID', 'Not set')
    g.client_secret = os.getenv('OAUTH_CLIENT_SECRET', 'Not set')
    g.consumer_key = os.getenv('OAUTH_CONSUMER_KEY', 'Not set')
    g.redirect_uri = os.getenv('REDIRECT_URI', 'Not set')
    g.token_path = os.getenv('TOKEN_PATH', 'Not set')

if __name__ == '__main__':
    # bind to localhost only
    host = "127.0.0.1"

    # bind to all interfaces
    #host = "0.0.0.0"

    port = 5000
    app.run(host=host, port=port, debug=True)
