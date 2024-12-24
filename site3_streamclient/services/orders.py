from schwab import auth, client
from flask import g

import httpx
import json

def place_order(symbol):
    print(f"services.orders.place_order [ entry ]")
    print(f"data received: {symbol}")
    return "order placed successfully"

def get_orders_for_account(hash_value, *, max_results=None, from_entered_datetime=None, to_entered_datetime=None, status=None):
    print(f"services.orders.get_orders_for_account [ entry ]")

    try:
        # Prepare parameters to pass to the third-party API
        params = {}
        if max_results:
            params['max_results'] = max_results
        if from_entered_datetime:
            params['from_entered_datetime'] = from_entered_datetime
        if to_entered_datetime:
            params['to_entered_datetime'] = to_entered_datetime
        if status:
            params['status'] = status

        # API authentication setup
        api_key = g.client_id
        app_secret = g.client_secret
        callback_url = g.redirect_uri
        token_path = g.token_path
        
        c = auth.easy_client(api_key, app_secret, callback_url, token_path)
        
        # Make the API call with parameters
        r = c.get_orders_for_account(hash_value, **params)  # Pass parameters as keyword arguments
        assert r.status_code == httpx.codes.OK, r.raise_for_status()
        data = r.json()

        # dev/debug
        print(json.dumps(data, indent=4))    

        return data  # Return the data from the API

    except Exception as e:
        # Log the error and return None if the call fails
        print(f"Error retrieving account: {e}")
        return None
        
def get_orders_for_all_linked_accounts(*, max_results=None, from_entered_datetime=None, to_entered_datetime=None, status=None):
    print(f"services.orders.get_orders_for_all_linked_accounts [ entry ]")

    # Prepare parameters to pass to the third-party API
    params = {}
    if max_results:
        params['max_results'] = max_results
    if from_entered_datetime:
        params['from_entered_datetime'] = from_entered_datetime
    if to_entered_datetime:
        params['to_entered_datetime'] = to_entered_datetime
    if status:
        params['status'] = status

    try:
        # API authentication setup
        api_key = g.client_id
        app_secret = g.client_secret
        callback_url = g.redirect_uri
        token_path = g.token_path
        
        c = auth.easy_client(api_key, app_secret, callback_url, token_path)
        
        # Make the API call with parameters
        r = c.get_orders_for_all_linked_accounts(**params)  # Pass parameters as keyword arguments
        assert r.status_code == httpx.codes.OK, r.raise_for_status()
        data = r.json()

        # dev/debug
        print(json.dumps(data, indent=4))    

        return data  # Return the data from the API

    except Exception as e:
        # Log the error and return None if the call fails
        print(f"Error retrieving orders for all linked accounts: {e}")
        return None
