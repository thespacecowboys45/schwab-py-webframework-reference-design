from schwab import auth, client
import json
from services.celery_app import celery  # Import the Celery instance from the main application
from services.redis_client import redis_client
import asyncio
import ssl
import time
import inspect


from schwab import auth, client
from schwab.streaming import StreamClient

# deprecate
from flask import g

STREAM_CLIENT_LATEST_DATA = "schwab_client_latest_data"

task_iterations = 0
streaming_flag = False


# Stream Client Task Template
FLAG_STREAM_CLIENT_TASK_IS_RUNNING = "FLAG_STREAM_CLIENT_TASK_IS_RUNNING"
FLAG_STREAM_CLIENT_TASK_STATUS = "FLAG_STREAM_CLIENT_TASK_STATUS"
FLAG_STREAM_CLIENT_TASK_RESULT = "FLAG_STREAM_CLIENT_TASK_RESULT"
STREAM_CLIENT_TASK_DATA = "STREAM_CLIENT_TASK_DATA"


# @TODO - dxb - deprecate / unused ???
# Function to process input and return a result
def process_quote_input(input_text):

    api_key = g.client_id
    app_secret = g.client_secret
    callback_url = g.redirect_uri
    token_path = g.token_path
    
    c = auth.easy_client(api_key, app_secret, callback_url, token_path)
    r = c.get_quote(input_text)
    r.raise_for_status()

    # dev/debug
    #print(json.dumps(r.json(), indent=4))

    lastPrice = parse_quote(r.json())

    return f"Processed quote for: {input_text}.  Last Price: {lastPrice}"

    def parse_quote(quote_json):
        print(f"parse_quote [ entry ]")

    # development / debug
    #print(json.dumps(quote_json, indent=4))
    
    # If we *know* the symbol we can use this code.
    # Extract lastPrice
    #last_price = quote_json['AAPL']['quote']['lastPrice']

    # If we *do not know* the symbol iterate over the response
    # Iterate over all keys in the dictionary
    for symbol, details in quote_json.items():    
        # Extract lastPrice for each symbol
        last_price = str(details.get('quote', {}).get('lastPrice'))
        if last_price:
            return last_price
        else:
            return 0.0



# #-------------------------- STREAM CLIENT CODE ----------------------------# #
SCHWAB_STREAM_CLIENT_FLAG_KEY = "schwab_stream_client_flag_key"


@celery.task
def schwab_start_stream_client_task(api_key, app_secret, callback_url, token_path, account_id, symbol):
    print(f"schwab_start_stream_client_task [ entry ] [ symbol: {symbol}]")
    result = "stub"



    
    print(f"schwab_start_stream_client_task [ get easy_client ]")

    c = auth.easy_client(api_key, app_secret, callback_url, token_path)

    print(f"schwab_start_stream_client_task [ easy_client created ]")

# dev code to see if client works
#    r = c.get_quote('AAPL')
#    r.raise_for_status()
    # dev/debug
#    print(json.dumps(r.json(), indent=4))

    # Create a custom SSL context
    ssl_context = ssl.create_default_context()

    # Disable SSL certificate verification (use with caution)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Alternatively, use certifi to set a trusted CA bundle
    # ssl_context = ssl.create_default_context(cafile=certifi.where())

    stream_client = StreamClient(c, account_id=account_id, ssl_context=ssl_context)

    print(f"schwab_start_stream_client_task [ stream_client created ]")




    async def read_stream():
        await stream_client.login()

        print(f"READ STREAM - STREAM CLIENT")

        def print_message(message):
            print(f"print_message() - STREAM CLIENT")

            #print(json.dumps(message, indent=4))
            parsed = process_stream_data(message)
            if parsed is not None:
                record_data(parsed)
            else:
                print(f"NON parsable message from STREAM_CLIENT")


        #           if redis_client.get(SCHWAB_STREAM_CLIENT_FLAG_KEY) == b"false":
        #               print(f"EXIT STREAM CLIENT TASK")
        #               raise asyncio.CancelledError()  # Trigger task cancellation

        # Always add handlers before subscribing because many streams start sending
        # data immediately after success, and messages with no handlers are dropped.

        # LEVEL 2 data        
        #        stream_client.add_nasdaq_book_handler(print_message)
        #        await stream_client.nasdaq_book_subs(['GOOG'])


        # LEVEL 1 data
        stream_client.add_level_one_equity_handler(print_message)
        await stream_client.level_one_equity_subs([symbol])

        # Periodically check the Redis flag for cancellation
        while redis_client.get(SCHWAB_STREAM_CLIENT_FLAG_KEY) == b"true":
            try:
                await asyncio.wait_for(stream_client.handle_message(), timeout=2)  # Timeout allows periodic check
            except asyncio.TimeoutError:
                # Continue checking Redis flag on timeout
                continue
            except asyncio.CancelledError:
                print("Stream client task is being cancelled.")
                break

                print("Stream client task has exited the loop due to Redis flag.")        



### METHOD 3 ( use new_event_loop then set_event_loop)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(read_stream())
    except Exception as e:
        print(f"Exception in schwab_start_stream_client_task: {e}")
    finally:

        # cleanup
        asyncio.set_event_loop(None)
        loop.close()

    print("schwab_start_stream_client_task [ exit ]")
    return result


#
# ---------------- SUPPORTING FUNCTIONS --------------------#
#

def process_stream_data(data):
    print(f"process_stream_data [ entry ]")
    
    #print(f"Process the data [ {data} ]")

    """
    Parses JSON data to extract 'key' and 'LAST_PRICE' values.
    Returns a list of JSON objects, each containing 'key' and 'LAST_PRICE'.
    Logs a message for any items without 'LAST_PRICE'.
    """
    parsed_data = []

    # Iterate over each element in the content array
    for item in data.get("content", []):
        # Extract 'key' and 'LAST_PRICE'
        key = item.get("key")
        last_price = item.get("LAST_PRICE")
        
        if key is None:
            print("Unparseable: missing 'key'")
            continue

        if last_price is None:
            print(f"Unparseable: 'LAST_PRICE' missing for key '{key}'")
            continue
        
        # Create payload for the JSON object
        payload = {
            "key": key,
            "LAST_PRICE": last_price
        }
        
        # Append payload to parsed data list
        parsed_data.append(payload)

    print(f"Processing complete: {parsed_data}")  

    if len(parsed_data) == 0:
        return None

    return parsed_data


# move this function to another module
"""
deprecated

def record_data(data):
    print(f"record_data() [ entry ] [ data: {data} ]")

    # Serialize data to JSON (if not already a string)
    data_json = json.dumps(data) if not isinstance(data, str) else data

    # Store in Redis with key 'STREAM_CLIENT_LATEST_DATA'
    redis_client.set(STREAM_CLIENT_LATEST_DATA, data_json)

    print(f"Data stored in Redis with key '{STREAM_CLIENT_LATEST_DATA}'")

    print(f"record_data() [ exit ]")
"""

# move this function to another module
def record_data_stream_client(data):
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")


    # Serialize data to JSON (if not already a string)
    data_json = json.dumps(data) if not isinstance(data, str) else data

    # Store in Redis with key 'STREAM_CLIENT_LATEST_DATA'
    redis_client.set(FLAG_STREAM_CLIENT_TASK_RESULT, data_json)
    redis_client.set(STREAM_CLIENT_LATEST_DATA, data_json)

    print(f"Data stored in Redis with key '{FLAG_STREAM_CLIENT_TASK_RESULT}'")

    print(f"record_data() [ exit ]")



#
# At the moment the result either either
# a) streaming data from the streaming client or
# b) an update to the task status because it was stopped or not started
#
def get_latest_data():
    print(f"get_latest_data() [ entry ]")
    # refactor to celery task
    #data = redis_client.get(STREAM_CLIENT_LATEST_DATA)
    data = redis_client.get(FLAG_STREAM_CLIENT_TASK_RESULT)

    if data is None:
        return jsonify({"error": "No data available"}), 404

    # Parse the data as a JSON object
    try:
        return json.loads(data.decode('utf-8')) # Decode bytes to string
    except json.JSONDecodeError:
        #return jsonify({"error": "Failed to parse data"}), 500
        return {"error": f"Failed to parse data: {data.decode('utf-8')}"}



# creates a stream of data using SSE for sending back to the client
def generateStreamClientDataStream():
    global streaming_flag
    print(f"generateStreamClientDataStream() [ entry ] [ streaming_flag : {streaming_flag} ]")


    while streaming_flag:
        data = get_latest_data()
        # 'yield' returns the data back directly to the client (browser)
        # NOTE: Data is already decoded, so no need to use json.dump() on it again
        yield f"data: {json.dumps(data)}\n\n" # Send data as SSE format
        time.sleep(1)
        print(f"Data streamed to client {data}")


# ------------------------------------------------------
# Porting over task template code to work with schwab-py streamClient
#
#########



@celery.task
def task_stream_client(api_key=None, app_secret=None, callback_url=None, token_path=None, account_id=None):
    global task_iterations

    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    redis_client.set(FLAG_STREAM_CLIENT_TASK_IS_RUNNING, "true")
    status = {"status":"running"}
    redis_client.set(FLAG_STREAM_CLIENT_TASK_STATUS, str(status))

    while redis_client.get(FLAG_STREAM_CLIENT_TASK_IS_RUNNING) == b"true":
        task_iterations += 1

        print(f"{ex_path} Automations Stream Client Task is running ... [ iterations: {task_iterations} ]")

        # Implement business logic
        do_work(api_key, app_secret, callback_url, token_path, account_id)

        result = {"status": "running", "iterations": task_iterations}
        redis_client.set(FLAG_STREAM_CLIENT_TASK_RESULT, json.dumps(result))  # Store the result in Redis   

        # I want to see what happens in this case, does do_work() exit after kicking off the async process ?
        print(f"{ex_path} DEBUG -------------------------------------------------------------")
        print(f"{ex_path} DEBUG -------------------------------------------------------------")
        print(f"{ex_path} DEBUG -------------------------------------------------------------")
        print(f"{ex_path} DEBUG -------------------------------------------------------------")
        print(f"{ex_path} DEBUG -------------------------------------------------------------")
        print(f"{ex_path} DEBUG -------------------------------------------------------------")

        # Simulate a long-running process
        time.sleep(5)

    status = {"status":"stopped"}
    redis_client.set(FLAG_STREAM_CLIENT_TASK_STATUS, str(status))
    result = {"status": "stopped", "iterations": task_iterations}

    print(f"{ex_path} DEBUG result: {result}")
    result_encoded = json.dumps(result)
    print(f"{ex_path} DEBUG result_encoded: {result_encoded}")

    redis_client.set(FLAG_STREAM_CLIENT_TASK_RESULT, result_encoded)  # Store the result in Redis        
    print(f"{ex_path} [ exit ]")


def do_work(api_key=None, app_secret=None, callback_url=None, token_path=None, account_id=None):
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    data = redis_client.get(STREAM_CLIENT_TASK_DATA)

    if data:
        decoded_symbols_list = data.decode('utf-8')
        print(f"{ex_path} [ process data ] [ decoded_symbols_list: {decoded_symbols_list}]")

        c = auth.easy_client(api_key, app_secret, callback_url, token_path)

        # Create a custom SSL context
        ssl_context = ssl.create_default_context()

        # Disable SSL certificate verification (use with caution)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Alternatively, use certifi to set a trusted CA bundle
        # ssl_context = ssl.create_default_context(cafile=certifi.where())

        stream_client = StreamClient(c, account_id=account_id, ssl_context=ssl_context)

        async def read_stream():
            await stream_client.login()

            print(f"READ STREAM - STREAM CLIENT")

            def print_message(message):
                print(f"print_message() - STREAM CLIENT")

                #print(json.dumps(message, indent=4))
                parsed = process_stream_data(message)
                if parsed is not None:
                    record_data_stream_client(parsed)
                else:
                    print(f"NON parsable message from STREAM_CLIENT")

            # LEVEL 1 data
            stream_client.add_level_one_equity_handler(print_message)
            await stream_client.level_one_equity_subs([decoded_symbols_list])

            # Periodically check the Redis flag for cancellation
            while redis_client.get(FLAG_STREAM_CLIENT_TASK_IS_RUNNING) == b"true":
                try:
                    await asyncio.wait_for(stream_client.handle_message(), timeout=2)  # Timeout allows periodic check
                except asyncio.TimeoutError:
                    # Continue checking Redis flag on timeout
                    continue
                except asyncio.CancelledError:
                    print("Stream client task is being cancelled.")
                    break

                    print("Stream client task has exited the loop due to Redis flag.")        

        ### METHOD 3 ( use new_event_loop then set_event_loop)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(read_stream())
        except Exception as e:
            print(f"Exception in schwab_start_stream_client_task: {e}")
        finally:

            # cleanup
            asyncio.set_event_loop(None)
            loop.close()

        print("schwab_start_stream_client_task [ exit ]")


    else:
        print(f"{ex_path} [ no data to process ]")

    print(f"{ex_path} DEBUG -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--==-=-=-=-=-=-=-=-=-=-=")
    print(f"{ex_path} DEBUG -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--==-=-=-=-=-=-=-=-=-=-=")
    print(f"{ex_path} DEBUG -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--==-=-=-=-=-=-=-=-=-=-=")
    print(f"{ex_path} DEBUG -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--==-=-=-=-=-=-=-=-=-=-=")
    print(f"{ex_path} DEBUG -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--==-=-=-=-=-=-=-=-=-=-=")
    print(f"{ex_path} DEBUG -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--==-=-=-=-=-=-=-=-=-=-=")



def init():
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    status = {"status": "init"}
    redis_client.set(FLAG_STREAM_CLIENT_TASK_STATUS, str(status))  # Store the result in Redis 

    result = {"result":"init"}
    redis_client.set(FLAG_STREAM_CLIENT_TASK_RESULT, str(result))  # Store the result in Redis 

    redis_client.set(FLAG_STREAM_CLIENT_TASK_IS_RUNNING, "false")

    print(f"{ex_path} [ task initialized ]")

