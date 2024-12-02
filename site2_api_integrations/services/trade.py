from schwab import auth, client, utils
import json
import inspect
import httpx

from flask import g


# Function to process input and return a result
def place_order(hash_value, order):
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")
    print(f"{ex_path} [ hash: {hash_value} ] [ order: {order} ]")
    

    api_key = g.client_id
    app_secret = g.client_secret
    callback_url = g.redirect_uri
    token_path = g.token_path
    

    #return json.dumps({"status":"stubbed out order {order} not placed"})

    #
    # From the docs:https://schwab-py.readthedocs.io/en/latest/client.html#placing-new-orders 
    # Place an order for a specific account. If order creation was successful, the response will contain the ID of the generated order. See schwab.utils.Utils.extract_order_id() for more details. Note unlike most methods in this library, responses for successful calls to this method typically do not contain json() data, and attempting to extract it will likely result in an exception.
    #
    c = auth.easy_client(api_key, app_secret, callback_url, token_path)
    r = c.place_order(hash_value, order)
    assert r.status_code in (httpx.codes.OK, httpx.codes.CREATED), r.raise_for_status()
    order_id = utils.Utils(client, hash_value).extract_order_id(r)
    assert order_id is not None

    # dev/debug
    print(f"{ex_path} order_id: {order_id}")

    return order_id
