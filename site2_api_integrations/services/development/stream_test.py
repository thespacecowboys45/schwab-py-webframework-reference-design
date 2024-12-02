# module_streaming.py
import time
import json
import os

latest_value = 0
streaming_active = False # Assume we are not streaming on startup.

# ################# STREAMING TEST implementation

# helper function for MAIN to use this value
def get_latest_value():
    global latest_value
    return latest_value

def get_dynamic_content():
    global latest_value

    print(f"get_dynamic_content [ entry ] [ latest_value: {latest_value} ] [ streaming_active: {streaming_active} ]")

    latest_value += 1
    # Return the data to send as an SSE message

    worker_pid = os.getpid()
    return {"lastPrice": latest_value, "workerPid": worker_pid}  # Replace with your actual data retrieval        

def generateStreamTest():
    global streaming_active, latest_value

    print(f"generateStreamTest [ entry ] [ streaming_active: {streaming_active} ]")
    while streaming_active:
        data = get_dynamic_content()
        # 'yield' returns the data back directly to the client (browser)
        yield f"data: {json.dumps(data)}\n\n"  # Send data as SSE format
        time.sleep(1)
        print(f"Data streamed to client {data}....")

def startStreamTest():
    global streaming_active, latest_value
    print(f"module_streaming [ startStreamTest() ] [ entry ] [ latest_value: {latest_value} ]")
    streaming_active = True  # Flag to start the stream

def stopStreamTest():
    global streaming_active, latest_value
    print(f"module_streaming [ stopStreamTest() ] [ entry ] [ latest_value: {latest_value} ]")
    streaming_active = False  # Flag to stop the stream


# ################# SCHWAB implementation