# login.py
from flask import g, session
import requests
import inspect

from schwab import auth

def createClientFromCallback(received_url):
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    print(f"{ex_path} [received_url={received_url}]")    
    client = getBearerToken(received_url)

    if client is None:
        print(f"createClient [ no client returned ]")
        return None
    else:
        print(f"createClient [ created a new client ]")
        return client

# Function to get bearer token using the code from URL and session
def getBearerToken(received_url):
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    print(f"{ex_path} [received_url={received_url}]")

    # Set variables
    token_path = g.token_path
    api_key = g.client_id
    app_secret = g.client_secret
    callback_url = g.redirect_uri
    asyncio = False
    enforce_enums = False
    token_write_func = None

    # retrieve the auth_context_state from the session, which was created on login (kinda)
    auth_context_state = session.get('auth_context_state')

    # NOTE: documentation purposes ...
    #
    # This is the CSRF token from the original authorization_url creation
    # It is used (again) when going back to schwab in order to authenticate
    # in the final steps of OAuth authentication process
    print(f"login.py [ getBearerToken ] [ auth_context_state : {auth_context_state} ]")
    # explicitly set the state
    auth_context = auth.get_auth_context(api_key, g.redirect_uri, auth_context_state)

    print(f"getBearerToken [ DEBUG: auth_context_state is {auth_context_state}]")

    token_write_func = (
        auth.__make_update_token_func(token_path) if token_write_func is None
        else token_write_func)

    return auth.client_from_received_url(
            api_key, app_secret, auth_context, received_url, token_write_func, 
            asyncio, enforce_enums)    