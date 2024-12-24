from schwab import auth, client
from flask import g

import httpx
import json
import inspect
import traceback

def convert_frequency_to_enum(client, text):
    """
    Convert a text input to the corresponding enum value.
    
    :param projection_text: Text representing the enum value.
    :return: Corresponding enum value or None if not found.
    """
    try:
        # Ensure the input matches the enum member name (case-sensitive)
        return client.PriceHistory.Frequency[text]
    except KeyError:
        # Handle invalid projection text gracefully
        raise ValueError(f"Invalid frequency: {text}. Must be one of: {[e.name for e in client.PriceHistory.Frequency]}")

def convert_frequency_type_to_enum(client, text):
    """
    Convert a text input to the corresponding enum value.
    
    :param projection_text: Text representing the enum value.
    :return: Corresponding enum value or None if not found.
    """
    try:
        # Ensure the input matches the enum member name (case-sensitive)
        return client.PriceHistory.FrequencyType[text]
    except KeyError:
        # Handle invalid projection text gracefully
        raise ValueError(f"Invalid frequency_type: {text}. Must be one of: {[e.name for e in client.PriceHistory.FrequencyType]}")

def convert_period_to_enum(client, text):
    """
    Convert a text input to the corresponding enum value.
    
    :param projection_text: Text representing the enum value.
    :return: Corresponding enum value or None if not found.
    """
    try:
        # Ensure the input matches the enum member name (case-sensitive)
        return client.PriceHistory.Period[text]
    except KeyError:
        # Handle invalid projection text gracefully
        raise ValueError(f"Invalid period: {text}. Must be one of: {[e.name for e in client.PriceHistory.Period]}")

def convert_period_type_to_enum(client, text):
    """
    Convert a text input to the corresponding enum value.
    
    :param projection_text: Text representing the enum value.
    :return: Corresponding enum value or None if not found.
    """
    try:
        # Ensure the input matches the enum member name (case-sensitive)
        return client.PriceHistory.PeriodType[text]
    except KeyError:
        # Handle invalid projection text gracefully
        raise ValueError(f"Invalid period_type: {text}. Must be one of: {[e.name for e in client.PriceHistory.PeriodType]}")

#
# schwab-py spec:
# Client.get_price_history(symbol, *, period_type=None, period=None, frequency_type=None, frequency=None, start_datetime=None, end_datetime=None, need_extended_hours_data=None, need_previous_close=None)
#
def get_price_history(symbol, *,  period_type=None, period=None, frequency_type=None, frequency=None, start_datetime=None, end_datetime=None, need_extended_hours_data=None, need_previous_close=None, store_data=None):
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")
    print(f"{ex_path} [ entry ] [ params symbol: {symbol} start_datetime: {start_datetime} ]")

    try:

        # API authentication setup
        api_key = g.client_id
        app_secret = g.client_secret
        callback_url = g.redirect_uri
        token_path = g.token_path
        
        c = auth.easy_client(api_key, app_secret, callback_url, token_path)

        # Prepare parameters to pass to the third-party API
        params = {}
        if period_type:
            try:
                period_type_enum = convert_period_type_to_enum(c, period_type)
                params['period_type'] = period_type_enum
            except Exception as e:
                print(f"{ex_path} There was an exception: {e}")

        if period:
            try:
                period_enum = convert_period_to_enum(c, period)
                params['period'] = period_enum
            except Exception as e:
                print(f"{ex_path} There was an exception: {e}")

        if frequency_type:
            try:
                frequency_type_enum = convert_frequency_type_to_enum(c, frequency_type)
                params['frequency_type'] = frequency_type_enum
            except Exception as e:
                print(f"{ex_path} There was an exception: {e}")

        if frequency:
            try:
                frequency_enum = convert_frequency_to_enum(c, frequency)
                params['frequency'] = frequency_enum
            except Exception as e:
                print(f"{ex_path} There was an exception: {e}")


        if start_datetime:
            params['start_datetime'] = start_datetime
        if end_datetime:
            params['end_datetime'] = end_datetime
        if need_extended_hours_data:
            params['need_extended_hours_data'] = need_extended_hours_data
        if need_previous_close:
            params['need_previous_close'] = need_previous_close

        print(f"{ex_path} INPUT: symbol={symbol} params={params}")


        
        # Make the API call with parameters
        r = c.get_price_history(symbol, **params)  # Pass parameters as keyword arguments
        assert r.status_code == httpx.codes.OK, r.raise_for_status()
        data = r.json()

        print(f"{ex_path} response data: {data}")
        
        return data  # Return the data from the API

    except Exception as e:
        # Log the error and return None if the call fails
        print(f"Error retrieving pricehistory: {e}")
        return None
  

# Modified to be used by a celery task (outside of application context)
# OR by a webapp using Flasks 'g' global namespace
def get_price_history_every_minute(symbol, *,  period_type=None, period=None, frequency_type=None, frequency=None, start_datetime=None, end_datetime=None, need_extended_hours_data=None, need_previous_close=None, store_data=None, api_key=None, app_secret=None, callback_url=None, token_path=None):
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ] [ symbol: {symbol} ]")
    print(f"{ex_path} [ entry ] [ symbol: {symbol} ]")

    try:
        # API authentication setup
        if api_key is None and app_secret is None:
            # Attempt to retrieve from Flask's global namespace
            if g and hasattr(g, 'client_id') and hasattr(g, 'client_secret') and hasattr(g, 'redirect_uri') and hasattr(g, 'token_path'):
                api_key = g.client_id
                app_secret = g.client_secret
                callback_url = g.redirect_uri
                token_path = g.token_path
            else:
                raise ValueError("API key, app secret, callback URL, and token path must be provided either through parameters or Flask's g context.")

        
        c = auth.easy_client(api_key, app_secret, callback_url, token_path)


        # Prepare parameters to pass to the third-party API
        params = {}
        if period_type:
            try:
                period_type_enum = convert_period_type_to_enum(c, period_type)
                params['period_type'] = period_type_enum
            except Exception as e:
                print(f"{ex_path} There was an exception: {e}")

            #params['period_type'] = period_type
        if period:
            try:
                period_enum = convert_period_to_enum(c, period)
                params['period_type'] = period_enum
            except Exception as e:
                print(f"{ex_path} There was an exception: {e}")


            #params['period'] = period
        if frequency_type:
            try:
                frequency_type_enum = convert_frequency_type_to_enum(c, frequency_type)
                params['frequency_type'] = frequency_type_enum
            except Exception as e:
                print(f"{ex_path} There was an exception: {e}")

            #params['frequency_type'] = frequency_type

        if frequency:
            try:
                frequency_enum = convert_frequency_to_enum(c, frequency)
                params['frequency'] = frequency_enum
            except Exception as e:
                print(f"{ex_path} There was an exception: {e}")

            #params['frequency'] = frequency


        if start_datetime:
            params['start_datetime'] = start_datetime
        if end_datetime:
            params['end_datetime'] = end_datetime
        if need_extended_hours_data:
            params['need_extended_hours_data'] = need_extended_hours_data
        if need_previous_close:
            params['need_previous_close'] = need_previous_close

        print(f"{ex_path} INPUT: symbol={symbol} params={params}")


        
        # Make the API call with parameters
        r = c.get_price_history_every_minute(symbol, **params)  # Pass parameters as keyword arguments
        assert r.status_code == httpx.codes.OK, r.raise_for_status()
        data = r.json()

        print(f"{ex_path} response data: {data}")

        return data  # Return the data from the API

    except Exception as e:
        # Log the error and return None if the call fails
        print(f"Error retrieving pricehistory: {e}")
        stack_trace = traceback.format_exc()
        print(f"Traceback:\n{stack_trace}")

        return None
  