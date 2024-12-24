from schwab import auth, client
from flask import g

import httpx
import json

def get_transactions(hash_value, *, start_date=None, end_date=None, transaction_type=None, symbol=None):
    print(f"services.transactions.get_transactions [ entry ]")

    try:
        # Prepare parameters to pass to the third-party API
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if transaction_type:
            params['transaction_type'] = transaction_type
        if symbol:
            params['symbol'] = symbol

        # API authentication setup
        api_key = g.client_id
        app_secret = g.client_secret
        callback_url = g.redirect_uri
        token_path = g.token_path
        
        c = auth.easy_client(api_key, app_secret, callback_url, token_path)
        
        # Make the API call with parameters
        r = c.get_transactions(hash_value, **params)  # Pass parameters as keyword arguments
        assert r.status_code == httpx.codes.OK, r.raise_for_status()
        data = r.json()

        # dev/debug
        print(json.dumps(data, indent=4))    

        return data  # Return the data from the API

    except Exception as e:
        # Log the error and return None if the call fails
        print(f"Error retrieving transactions: {e}")
        return None