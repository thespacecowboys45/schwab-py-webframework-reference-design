from schwab import auth, client
from flask import g

import httpx
import json

import inspect

# @TODO - move this 
from services.quotes import parse_quote


def get_account_numbers():
    print(f"accounts.py [ get_account_numbers() ] [ entry ]")
    input_text = 'AAPL'

    api_key = g.client_id
    app_secret = g.client_secret
    callback_url = g.redirect_uri
    token_path = g.token_path
    
    c = auth.easy_client(api_key, app_secret, callback_url, token_path)
    r = c.get_account_numbers()
    r.raise_for_status()

    # dev/debug
    #print(json.dumps(r.json(), indent=4))

    return r.json()

# Assuming you're interacting with a 3rd party API, define this function
def get_account(hash_value):
    # Example of how you might call the 3rd-party API using the hashValue
    try:

        api_key = g.client_id
        app_secret = g.client_secret
        callback_url = g.redirect_uri
        token_path = g.token_path
        
        c = auth.easy_client(api_key, app_secret, callback_url, token_path)
        r = c.get_account(hash_value)
        assert r.status_code == httpx.codes.OK, r.raise_for_status()
        data = r.json()

        # dev/debug
        print(json.dumps(data, indent=4))    

        return data  # Return the data from the API

    except Exception as e:
        # Log the error and return None if the call fails
        print(f"Error retrieving account: {e}")
        return None

def get_accounts():
    print(f"accounts.py [ get_accounts() ] [ entry ]")
    input_text = 'AAPL'

    api_key = g.client_id
    app_secret = g.client_secret
    callback_url = g.redirect_uri
    token_path = g.token_path
    
    c = auth.easy_client(api_key, app_secret, callback_url, token_path)
    r = c.get_accounts()
    r.raise_for_status()


    # dev/debug
    print(json.dumps(r.json(), indent=4))    

    return r.json() 

def get_user_preferences():
    print(f"{__name__} [ entry ]")

    api_key = g.client_id
    app_secret = g.client_secret
    callback_url = g.redirect_uri
    token_path = g.token_path
    
    c = auth.easy_client(api_key, app_secret, callback_url, token_path)
    r = c.get_user_preferences()
    r.raise_for_status()


    # dev/debug
    print(json.dumps(r.json(), indent=4))    

    return r.json()    

def get_positions(hash_value):
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    try:

        api_key = g.client_id
        app_secret = g.client_secret
        callback_url = g.redirect_uri
        token_path = g.token_path
        
        c = auth.easy_client(api_key, app_secret, callback_url, token_path)

        print(f"{ex_path} DEBUG: {c.Account.Fields.POSITIONS}")
        print(f"{ex_path} DEBUG: {c.Account.Fields.POSITIONS.value}")


        #r = c.get_account(hash_value, c.Account.Fields.POSITIONS)
        r = c.get_account(hash_value, fields=c.Account.Fields.POSITIONS)
        assert r.status_code == httpx.codes.OK, r.raise_for_status()
        data = r.json()

        # dev/debug
        print(json.dumps(data, indent=4))    

        return data  # Return the data from the API

    except Exception as e:
        # Log the error and return None if the call fails
        print(f"Error retrieving account: {e}")
        return None
