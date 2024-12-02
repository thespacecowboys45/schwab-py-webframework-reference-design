from schwab import auth, client
import json
import inspect

from flask import g

def convert_projection_to_enum(client, projection_text):
    """
    Convert a text input to the corresponding Instrument.Projection enum value.
    
    :param projection_text: Text representing the projection.
    :return: Corresponding enum value or None if not found.
    """
    try:
        # Ensure the input matches the enum member name (case-sensitive)
        return client.Instrument.Projection[projection_text]
    except KeyError:
        # Handle invalid projection text gracefully
        raise ValueError(f"Invalid projection: {projection_text}. Must be one of: {[e.name for e in client.Instrument.Projection]}")

def convert_index_to_enum(client, index_text):
    """
    Convert a text input to the corresponding Movers.Index enum value.
    
    :param index_text: Text representing the index.
    :return: Corresponding enum value or None if not found.
    """
    try:
        # Ensure the input matches the enum member name (case-sensitive)
        return client.Movers.Index[index_text]
    except KeyError:
        # Handle invalid projection text gracefully
        raise ValueError(f"Invalid index: {index_text}. Must be one of: {[e.name for e in client.Movers.Index]}")

def convert_sortorder_to_enum(client, sortorder_text):
    """
    Convert a text input to the corresponding Movers.SortOrder enum value.
    
    :param sortorder_text: Text representing the sortorder.
    :return: Corresponding enum value or None if not found.
    """
    try:
        # Ensure the input matches the enum member name (case-sensitive)
        return client.Movers.SortOrder[sortorder_text]
    except KeyError:
        # Handle invalid projection text gracefully
        raise ValueError(f"Invalid sortorder: {sortorder_text}. Must be one of: {[e.name for e in client.Movers.SortOrder]}")

def convert_frequency_to_enum(client, frequency_text):
    """
    Convert a text input to the corresponding Movers.Frequency enum value.
    
    :param frequency_text: Text representing the frequency.
    :return: Corresponding enum value or None if not found.
    """
    try:
        # Ensure the input matches the enum member name (case-sensitive)
        return client.Movers.Frequency[frequency_text]
    except KeyError:
        # Handle invalid projection text gracefully
        raise ValueError(f"Invalid frequency: {frequency_text}. Must be one of: {[e.name for e in client.Movers.Frequency]}")


def convert_market_to_enum(client, market_text):
    """
    Convert a text input to the corresponding MarketHours.Market enum value.
    
    :param market_text: Text representing the market.
    :return: Corresponding enum value or None if not found.
    """
    try:
        # Ensure the input matches the enum member name (case-sensitive)
        return client.MarketHours.Market[market_text]
    except KeyError:
        # Handle invalid projection text gracefully
        raise ValueError(f"Invalid market: {market_text}. Must be one of: {[e.name for e in client.MarketHours.Market]}")



def get_instruments(symbol, projection_text):
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    print(f"symbol: {symbol}, projection: {projection_text}")

    api_key = g.client_id
    app_secret = g.client_secret
    callback_url = g.redirect_uri
    token_path = g.token_path
    
    c = auth.easy_client(api_key, app_secret, callback_url, token_path)

    # Convert the text to an enum
    try:
        projection_enum = convert_projection_to_enum(c, projection_text)
        print(f"Converted projection: {projection_enum}")
    except ValueError as e:
        print(e)    

    r = c.get_instruments(symbol, projection_enum)
    r.raise_for_status()

    # dev/debug
    data = r.json()
    print(json.dumps(data, indent=4))

    return data    



def get_movers(index, sortorder, frequency):
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    print(f"index: {index}, sortorder: {sortorder}, frequency: {frequency}")

    api_key = g.client_id
    app_secret = g.client_secret
    callback_url = g.redirect_uri
    token_path = g.token_path

    c = auth.easy_client(api_key, app_secret, callback_url, token_path)


    # Convert the text to an enum
    try:
        index_enum = convert_index_to_enum(c, index)
        print(f"Converted: {index_enum}")
    except ValueError as e:
        print(e)      

    # Convert the text to an enum
    try:
        sortorder_enum = convert_sortorder_to_enum(c, sortorder)
        print(f"Converted: {sortorder_enum}")
    except ValueError as e:
        print(e)    

    # Convert the text to an enum
    try:
        frequency_enum = convert_frequency_to_enum(c, frequency)
        print(f"Converted: {frequency_enum}")
    except ValueError as e:
        print(e)                      


    r = c.get_movers(index_enum, sort_order=sortorder_enum, frequency=frequency_enum)
    r.raise_for_status()

    # dev/debug
    data = r.json()
    print(json.dumps(data, indent=4))

    return data


def get_market_hours(market, *, date=None):
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    print(f"market: {market}, date: {date}")

    api_key = g.client_id
    app_secret = g.client_secret
    callback_url = g.redirect_uri
    token_path = g.token_path

    c = auth.easy_client(api_key, app_secret, callback_url, token_path)


    # Convert the text to an enum
    try:
        market_enum = convert_market_to_enum(c, market)
        print(f"Converted: {market_enum}")
    except ValueError as e:
        print(e)      

    r = c.get_market_hours(market_enum, date=date)
    r.raise_for_status()

    # dev/debug
    data = r.json()
    print(json.dumps(data, indent=4))

    return data
