from schwab import auth, client
import json

from flask import g


# Function to process input and return a result
def get_quote(input_text):
    print(f"quotes.py [ get_quote ] [ entry ]")

    api_key = g.client_id
    app_secret = g.client_secret
    callback_url = g.redirect_uri
    token_path = g.token_path
    
    c = auth.easy_client(api_key, app_secret, callback_url, token_path)
    r = c.get_quote(input_text)
    r.raise_for_status()

    # dev/debug
    print(json.dumps(r.json(), indent=4))

    # dev/debug
    data = r.json()
    print(json.dumps(data, indent=4))

    return data

# refactor.  perform this task client-side
#    lastPrice = parse_quote(r.json())
#
#    return f"Processed quote for: {input_text}.  Last Price: {lastPrice}"

# Function to process input and return a result
def get_quotes(input_text):
    print(f"quotes.py [ get_quotes ] [ entry ]")

    api_key = g.client_id
    app_secret = g.client_secret
    callback_url = g.redirect_uri
    token_path = g.token_path
    
    c = auth.easy_client(api_key, app_secret, callback_url, token_path)
    r = c.get_quotes(input_text)
    r.raise_for_status()

    # dev/debug
    data = r.json()
    print(json.dumps(data, indent=4))

    return data
  

def parse_quote(quote_json):
    print(f"quotes.py [ parse_quote ] [ entry ]")

    # development / debug
    print(json.dumps(quote_json, indent=4))
    
    # If we *know* the symbol we can use this code.
    # Extract lastPrice
    #last_price = quote_json['AAPL']['quote']['lastPrice']

    # If we *do not know* the symbol iterate over the response
    # Iterate over all keys in the dictionary
    for symbol, details in quote_json.items():    
        print(f"process item for symbol {symbol}")
        # Extract lastPrice for each symbol
        last_price = str(details.get('quote', {}).get('lastPrice'))

        print(f"last_price={last_price}")
        if last_price:
            return last_price
        else:
            return 0.0
