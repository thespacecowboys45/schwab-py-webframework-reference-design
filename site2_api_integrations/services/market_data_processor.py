# Code to handle processing beyond the scope of "getting data"
# This is the "process the data we got" code
import json
import os
import time

from services.redis_client import redis_client

STREAM_CLIENT_LATEST_DATA = "schwab_client_latest_data"

# Flags to control streaming
streaming_flag = False

'''
write python code to parse this json data.  
parse out the 'key' and 'LAST_PRICE' and , for each element in content create a new .json 
payload with an array of elements for each 'key' pulled out.

Additionally if there is no 'LAST_PRICE' key, then print a message out to the terminal stating "unparseable"


{
    "service": "LEVELONE_EQUITIES",
    "timestamp": 1731425540364,
    "command": "SUBS",
    "content": [
        {
            "key": "AMD",
            "LAST_PRICE": 145.5701,
            "TOTAL_VOLUME": 8155112,
            "LAST_SIZE": 150,
            "NET_CHANGE": -1.7799,
            "REGULAR_MARKET_LAST_PRICE": 145.5701,
            "REGULAR_MARKET_LAST_SIZE": 150,
            "REGULAR_MARKET_NET_CHANGE": -1.7799,
            "MARK": 145.5701,
            "QUOTE_TIME_MILLIS": 1731425539957,
            "TRADE_TIME_MILLIS": 1731425539930,
            "REGULAR_MARKET_TRADE_MILLIS": 1731425539930,
            "BID_TIME_MILLIS": 1731425539957,
            "NET_CHANGE_PERCENT": -1.20794028,
            "REGULAR_MARKET_CHANGE_PERCENT": -1.20794028,
            "MARK_CHANGE": -1.7799,
            "MARK_CHANGE_PERCENT": -1.20794028
        }
    ]
}


'''

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
def record_data(data):
    print(f"record_data() [ entry ] [ data: {data} ]")

    # Serialize data to JSON (if not already a string)
    data_json = json.dumps(data) if not isinstance(data, str) else data

    # Store in Redis with key 'STREAM_CLIENT_LATEST_DATA'
    redis_client.set(STREAM_CLIENT_LATEST_DATA, data_json)

    print(f"Data stored in Redis with key '{STREAM_CLIENT_LATEST_DATA}'")

    print(f"record_data() [ exit ]")

def get_latest_data():
    print(f"get_latest_data() [ entry ]")
    data = redis_client.get(STREAM_CLIENT_LATEST_DATA)

    if data is None:
        return jsonify({"error": "No data available"}), 404

    # Parse the data as a JSON object
    try:
        return json.loads(data.decode('utf-8')) # Decode bytes to string
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse data"}), 500


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

