from schwab import auth, client
from flask import g

import httpx
import json
import inspect

#
# schwab-py spec:
# Client.get_price_history(symbol, *, period_type=None, period=None, frequency_type=None, frequency=None, start_datetime=None, end_datetime=None, need_extended_hours_data=None, need_previous_close=None)
#
def get_price_history(symbol, *,  period_type=None, period=None, frequency_type=None, frequency=None, start_datetime=None, end_datetime=None, need_extended_hours_data=None, need_previous_close=None):
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    try:
        # Prepare parameters to pass to the third-party API
        params = {}
        if period_type:
            params['period_type'] = period_type
        if period:
            params['period'] = period
        if frequency_type:
            params['frequency_type'] = frequency_type
        if frequency:
            params['frequency'] = frequency
        if start_datetime:
            params['start_datetime'] = start_datetime
        if end_datetime:
            params['end_datetime'] = end_datetime
        if need_extended_hours_data:
            params['need_extended_hours_data'] = need_extended_hours_data
        if need_previous_close:
            params['need_previous_close'] = need_previous_close

        print(f"{ex_path} INPUT: symbol={symbol} params={params}")

        # API authentication setup
        api_key = g.client_id
        app_secret = g.client_secret
        callback_url = g.redirect_uri
        token_path = g.token_path
        
        c = auth.easy_client(api_key, app_secret, callback_url, token_path)
        
        # Make the API call with parameters
        r = c.get_price_history(symbol, **params)  # Pass parameters as keyword arguments
        assert r.status_code == httpx.codes.OK, r.raise_for_status()
        data = r.json()

        # dev/debug
        #print(json.dumps(data, indent=4))    

        return data  # Return the data from the API

    except Exception as e:
        # Log the error and return None if the call fails
        print(f"Error retrieving pricehistory: {e}")
        return None
  