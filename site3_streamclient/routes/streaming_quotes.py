from flask import Blueprint, render_template, Response, request, jsonify, g, session
import os
import json
import inspect

from services.redis_client import redis_client
import services.celery_app

from services.stream_client import process_quote_input
from services.stream_client import schwab_start_stream_client_task
from services.stream_client import SCHWAB_STREAM_CLIENT_FLAG_KEY

from services import stream_client as sc
from services.stream_client import STREAM_CLIENT_LATEST_DATA, streaming_flag, generateStreamClientDataStream

streaming_quotes_bp = Blueprint('streaming_quotes', __name__,  url_prefix='/streaming_quotes')





###########################################
# #--------# SCHWAB STREAMING #-------#####
###########################################
@streaming_quotes_bp.route('/')
def home():
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")  

    if redis_client.get(sc.FLAG_STREAM_CLIENT_TASK_IS_RUNNING) == b"true":
        stream_client_status = "running"
    else:
        stream_client_status = "not running"

    try:
        # Retrieve data from Redis
        symbols_list = redis_client.get(sc.STREAM_CLIENT_TASK_DATA)

        if not symbols_list:
            print(f"{ex_path} symbols list is not set")
            symbols_list = ""
        else:
            symbols_list = symbols_list.decode('utf-8')
            print(f"{ex_path} symbols list {symbols_list} ")


        return render_template('quotes/streaming_quotes.html', base_template=g.base_template, title="Streaming Quotes", stream_client_status=stream_client_status, symbols_list=symbols_list)

    except Exception as e:
        stack_trace = traceback.format_exc()
        #dlog.error(f"Streaming Quotes Failed to render page. Error: {str(e)}", extra=dlog_event_type_route)
        #dlog.error(f"Traceback:\n{stack_trace}", extra=dlog_event_type_route)
        return "An error occurred while rendering the watchlists page.", 500        



@streaming_quotes_bp.route('/schwab_start_stream_client', methods=['POST'])
def schwab_start_stream_client():
    stream_status = 'starting'

    # Check if 'hashValue' exists in the session
    accountNumber = session.get('accountNumber')
    if not accountNumber:
        return jsonify({'message': 'No account selected', 'order_data': None}), 200

    if redis_client.get(SCHWAB_STREAM_CLIENT_FLAG_KEY) == b"true":
        print(f"schwab_stream_start_client - FLAG is already set.  cannot start again.")
        msg = "Stream client already running.  Cannot start again."
        return msg

    redis_client.set(SCHWAB_STREAM_CLIENT_FLAG_KEY, "true")


    api_key = g.client_id
    app_secret = g.client_secret
    callback_url = g.redirect_uri
    token_path = g.token_path    
    #account_id = g.account_id


    # Get the symbol from the JSON payload in the request
    data = request.get_json()
#    symbol = data.get('symbol', 'AAPL')  # Use 'AAPL' as a default symbol if none is provided
    symbol = data.get('symbol') if data.get('symbol') else 'AAPL'  # Default to 'AAPL' if None or empty



    # check if logged in
    if os.path.exists(token_path):
        print(f"schwab_start_stream_client [ user is logged in ] [ start stream for symbol '{symbol}' ]")
        msg = "Stream client starting"

        # mark the task status as running

        task = schwab_start_stream_client_task.apply_async(args=[api_key, app_secret, callback_url, token_path, accountNumber, symbol])

        #task = schwab_start_stream_client_task.apply_async()  # Start the task asynchronously


    else:
        msg = "You are not logged in"

    return msg


@streaming_quotes_bp.route('/schwab_stop_stream_client', methods=['POST'])
def schwab_stop_stream_client():

    if redis_client.get(SCHWAB_STREAM_CLIENT_FLAG_KEY) == b"false":
        msg = "Stream client is not started.  Cannot re-stop it."
    else:
        redis_client.set(SCHWAB_STREAM_CLIENT_FLAG_KEY, "false")
        msg = "Stream client stopping"

    return msg


@streaming_quotes_bp.route('/schwab_get_latest_stream_client_data', methods=['GET'])
def schwab_get_latest_stream_client_data():
    # Try to retrieve the latest data from Redis
    data = redis_client.get(STREAM_CLIENT_LATEST_DATA)

    if data is None:
        return jsonify({"error": "No data found"}), 404

    # Parse the data as a JSON object
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse data"}), 500

    # Return the data back to the client
    return jsonify(data)    





# ###################### STREAM BACK STREAMING DATA ##############


## @TODO - do not need this route
'''
@schwab_bp.route('/schwab_start_stream_latest_data', methods=['POST'])
def schwab_start_stream_latest_data():
    global streaming_flag
    streaming_flag = True
    return "Streaming started", 200
'''

@streaming_quotes_bp.route('/schwab_stop_stream_latest_data', methods=['POST'])
def schwab_stop_stream_latest_data():
    # deprecate this
    #global streaming_flag
    #streaming_flag = False

    sc.streaming_flag = False

    return "Streaming stopped", 200

# route that handles the actual streaming of data
@streaming_quotes_bp.route('/schwab_stream_latest_data', methods=['GET'])
def schwab_stream_latest_data():
    # No!  Does not work like this
    #global streaming_flag

    # There is issue with global variables defined in other files
    # Access the namespace for this variable by referencing it directly here
    # OTHERWISE: This will not actually change the value of the variable
    
    # deprecate this reference
    #market_data_processor.streaming_flag = True

    sc.streaming_flag = True

    # response to the client with the data stream
    return Response(generateStreamClientDataStream(), content_type='text/event-stream')

'''    
    if not streaming_flag:
        return jsonify({"error": "Streaming is not active"}), 400
    
    # Retrieve the data from Redis
    data = redis_client.get('STREAM_CLIENT_LATEST_DATA')
    
    if data is None:
        return jsonify({"error": "No data available"}), 404
    
    # Send data back as a stream of JSON objects
    return jsonify({"data": data.decode()}), 200

'''



# ###################### ASYNCIO INTEGRATION ##############
# Start task route
@streaming_quotes_bp.route('/schwab_start_asyncio_task', methods=['POST'])
def schwab_start_asyncio_task():
    print("schwab_start_asyncio_task [ entry ]")
    if redis_client.get(SCHWAB_TASK_ASYNCIO_FLAG_KEY) == b"true":
        return jsonify({"status": "already running"}), 200

    task = schwab_asyncio_task.apply_async()  # Start the task asynchronously

    print("Starting background task...")
    return jsonify({"status": "started"}), 200

# Stop task route
@streaming_quotes_bp.route('/schwab_stop_asyncio_task', methods=['POST'])
def schwab_stop_asyncio_task():
    # Attempt to stop task (Celery doesn't support terminating a task directly)
    # This is a placeholder to simulate stopping a task.
    # For true task termination, use a workaround with task timeouts or a termination flag.
    print("Stopping schwab background task...")
    redis_client.set(SCHWAB_TASK_ASYNCIO_FLAG_KEY, "false")
    return jsonify({"status": "stopped"}), 200


@streaming_quotes_bp.route('/schwab_get_task_asyncio_result', methods=['POST'])
def schwab_get_task_asyncio_result():
    result = redis_client.get("schwab_asyncio_task_result")
    if result:
        return jsonify({"status": "success", "schwab_asyncio_task_result": result.decode('utf-8')}), 200
    else:
        return jsonify({"status": "no result", "schwab_asyncio_task_result": None}), 404        


# ---------------------------------------------------------------------------------------

# ported here from 'routes/automations'

@streaming_quotes_bp.route('/set_symbols_list', methods=['POST'])
def set_symbols_list():
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")  

    try:
        # Parse JSON data from the request
        request_data = request.get_json()
        symbols = request_data.get('symbols', '')

        print(f"set_symbols_list [ entry ] [ symbols: {symbols} ]")

        if not symbols:
            return jsonify({"error": "Symbols list cannot be empty"}), 400

        # Sanitize the symbols: uppercase, remove spaces between commas
        sanitized_symbols = ",".join(symbol.strip().upper() for symbol in symbols.split(","))

        # Store in Redis
        redis_client.set(sc.STREAM_CLIENT_TASK_DATA, sanitized_symbols)

        return jsonify({"status": "Symbols list set", "data": sanitized_symbols}), 200
    except Exception as e:
        print(f"set_symbols_list [ ERROR ] [{e}]")
        return jsonify({"error": str(e)}), 500

@streaming_quotes_bp.route('/get_symbols_list', methods=['POST'])
def get_symbols_list():   
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")  

    try:
        # Retrieve data from Redis
        symbols_list = redis_client.get(sc.STREAM_CLIENT_TASK_DATA)

        if not symbols_list:
            return jsonify({"status": "Symbols list is not set"}), 200

        # Decode and send the symbols list
        return jsonify({"status": "Symbols list retrieved", "data": symbols_list.decode('utf-8')}), 200
    except Exception as e:
        print(f"get_symbols_list [ ERROR ] [{e}]")
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------------------

# Start task route
@streaming_quotes_bp.route('/celery_start_template_task', methods=['POST'])
def celery_start_template_task():
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    requestData = request.get_json()
    taskName = requestData.get('taskName')

    api_key = g.client_id
    app_secret = g.client_secret
    callback_url = g.redirect_uri
    token_path = g.token_path

    print(f"{ex_path} celery_start_template_task [ entry ] [ taskName: {taskName} ]")

    # Check if 'hashValue' exists in the session
    accountNumber = session.get('accountNumber')
    if not accountNumber:
        response = {
            "running_status": 'No account selected',
            "task_status": "unknown",
            "task_result": "unknown"
        }

        return response, 200

    # First check if celery is running
    if not services.celery_app.is_celery_running():
        return jsonify({"running_status": "celery is not running yo", "task_status":"unknown", "task_result":"unknown"}), 200

    # Pythons version of a switch statement
    match taskName:
        case "stream_client":
            status = redis_client.get(sc.FLAG_STREAM_CLIENT_TASK_STATUS)
            result = redis_client.get(sc.FLAG_STREAM_CLIENT_TASK_RESULT)

            if redis_client.get(sc.FLAG_STREAM_CLIENT_TASK_IS_RUNNING) == b"true":
                return jsonify({"running_status": "already running", "task_status":status.decode('utf-8') if status else "unknown", "task_result":result.decode('utf-8') if result else "unknown"}), 200
            else:
                task = sc.task_stream_client.apply_async(args=[api_key, app_secret, callback_url, token_path, accountNumber])  # Start the task asynchronously

            task_set_to_run = redis_client.get(sc.FLAG_STREAM_CLIENT_TASK_IS_RUNNING)
        case _:
            print(f"{ex_path} Unknown task type requested to be started: {taskName}")
            return jsonify({"running_status": "unknown task " + taskName + " requested to be started", "task_status":"unknown", "task_result":"unknown"}), 200            

    if task_set_to_run:
        running_status = task_set_to_run.decode('utf-8')
        task_status = status.decode('utf-8') if status else "unknown"
        task_result = result.decode('utf-8') if result else "unknown"
    else:
        running_status = "no status"
        task_status = "unknown"
        task_result = "unknown"

    response = {
        "running_status": running_status,
        "task_status": task_status,
        "task_result": task_result
    }

    return jsonify(response), 200


# Stop task route
@streaming_quotes_bp.route('/celery_stop_template_task', methods=['POST'])
def celery_stop_template_task():
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    requestData = request.get_json()
    taskName = requestData.get('taskName')

    print(f"{ex_path} celery_stop_template_task [ entry ] [ taskName: {taskName} ]")

    # First check if celery is running
    if not services.celery_app.is_celery_running():
        return jsonify({"running_status": "celery is not running yo", "task_status":"unknown", "task_result":"unknown"}), 200

    # Pythons version of a switch statement
    match taskName:
        case "stream_client":
            redis_client.set(sc.FLAG_STREAM_CLIENT_TASK_IS_RUNNING, "false")

            task_set_to_run = redis_client.get(sc.FLAG_STREAM_CLIENT_TASK_IS_RUNNING)
            status = redis_client.get(sc.FLAG_STREAM_CLIENT_TASK_STATUS)
            result = redis_client.get(sc.FLAG_STREAM_CLIENT_TASK_RESULT)
        case _:
            print(f"{ex_path} Unknown task type requested to be stopped: {taskName}")
            return jsonify({"running_status": "unknown task " + taskName + " requested to be started", "task_status":"unknown", "task_result":"unknown"}), 200            

    if task_set_to_run:
        running_status = task_set_to_run.decode('utf-8')
        task_status = status.decode('utf-8') if status else "unknown"
        task_result = result.decode('utf-8') if result else "unknown"
    else:
        running_status = "no status"
        task_status = "unknown"
        task_result = "unknown"

    response = {
        "running_status": running_status,
        "task_status": task_status,
        "task_result": task_result
    }

    return jsonify(response), 200


@streaming_quotes_bp.route('/celery_get_template_task_status', methods=['POST'])
def celery_get_template_task_status():
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    requestData = request.get_json()
    taskName = requestData.get('taskName')

    print(f"{ex_path} celery_stop_template_task [ entry ] [ taskName: {taskName} ]")

    # First check if celery is running
    if not services.celery_app.is_celery_running():
        return jsonify({"running_status": "celery is not running yo", "task_status":"", "task_result":""}), 200

    # Pythons version of a switch statement
    match taskName:
        case "stream_client":
            task_set_to_run = redis_client.get(sc.FLAG_STREAM_CLIENT_TASK_IS_RUNNING)
            status = redis_client.get(sc.FLAG_STREAM_CLIENT_TASK_STATUS)
            result = redis_client.get(sc.FLAG_STREAM_CLIENT_TASK_RESULT)
        case _:
            return jsonify({"running_status": "unknown task " + taskName + " request for status", "task_status":"", "task_result":""}), 200            

    if task_set_to_run:
        running_status = task_set_to_run.decode('utf-8')
        task_status = status.decode('utf-8') if status else "unknown"
        task_result = result.decode('utf-8') if result else "unknown"
    else:
        running_status = "no status"
        task_status = "unknown"
        task_result = "unknown"

    response = {
        "running_status": running_status,
        "task_status": task_status,
        "task_result": task_result
    }

    return jsonify(response), 200

