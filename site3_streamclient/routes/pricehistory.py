from flask import Blueprint, render_template, session, jsonify, request, g
import services.pricehistory
from datetime import datetime
import inspect

pricehistory_bp = Blueprint('pricehistory', __name__, url_prefix='/pricehistory')

@pricehistory_bp.route('/')
def home():
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    return render_template('pricehistory/pricehistory.html', base_template=g.base_template)


@pricehistory_bp.route('/get_price_history', methods=['POST'])
def get_price_history():
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    # Check if 'hashValue' exists in the session
    hash_value = session.get('hashValue')
    if not hash_value:
        return jsonify({'message': 'No account selected', 'price_history_data': None}), 200

    # Extract parameters from the request JSON body
    params = request.get_json() or {}
    symbol = params.get('symbol').upper()
    start_datetime_str = params.get('start_datetime')
    end_datetime_str = params.get('end_datetime')
    status = params.get('status')

    print(f"{ex_path} params: {params}")
    #print(f"{ex_path} Received params: symbol={symbol}, start_datetime={start_datetime}, "
    #      f"end_datetime={end_datetime}, status={status}")


    # Convert datetime strings to datetime objects
    try:
        if start_datetime_str:
            params['start_datetime'] = datetime.fromisoformat(start_datetime_str)
        if end_datetime_str:
            params['end_datetime'] = datetime.fromisoformat(end_datetime_str)
    except ValueError as e:
        print(f"{ex_path} Invalid datetime format: {e}")
        return jsonify({'message': 'Invalid datetime format', 'price_history_data': None}), 400


    # Call the service function with the extracted parameters
#    price_history_data = services.pricehistory.get_price_history(
#        symbol=symbol
#    )
    price_history_data = services.pricehistory.get_price_history(
        **params
    )


    # Return both data and message
    if price_history_data:
        return jsonify({
            'message': 'Price History retrieved successfully',
            'price_history_data': price_history_data
        }), 200
    else:
        return jsonify({
            'message': 'Failed to retrieve pricehistory information',
            'price_history_data': None
        }), 500

@pricehistory_bp.route('/get_price_history2', methods=['POST'])
def get_price_history2():
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    # Check if 'hashValue' exists in the session
    hash_value = session.get('hashValue')
    if not hash_value:
        return jsonify({'message': 'No account selected', 'price_history_data': None}), 200

    # Extract parameters from the request JSON body
    params = request.get_json() or {}
    symbol = params.get('symbol').upper()
    start_datetime_str = params.get('start_datetime')
    end_datetime_str = params.get('end_datetime')
    
    print(f"{ex_path} params: {params}")

    # Convert datetime strings to datetime objects
    try:
        if start_datetime_str:
            params['start_datetime'] = datetime.fromisoformat(start_datetime_str)
        if end_datetime_str:
            params['end_datetime'] = datetime.fromisoformat(end_datetime_str)
    except ValueError as e:
        print(f"{ex_path} Invalid datetime format: {e}")
        return jsonify({'message': 'Invalid datetime format', 'price_history_data': None}), 400

    # Call the service function with the extracted parameters
    try:
        print(f"{ex_path} call service get_price_history with params: {params}")
        price_history_data = services.pricehistory.get_price_history(**params)
    except Exception as e:
        print(f"{ex_path} There was an exception: {e}")
        return jsonify({
            'message': 'Failed to retrieve pricehistory information',
            'price_history_data': None
        }), 500

    #print(f"{ex_path} price_history_data: {price_history_data}")

    # Return both data and message
    if price_history_data:
        return jsonify({
            'message': 'Price History retrieved successfully',
            'price_history_data': price_history_data
        }), 200
    else:
        return jsonify({
            'message': 'Failed to retrieve pricehistory information',
            'price_history_data': None
        }), 500


@pricehistory_bp.route('/get_price_history_every_minute', methods=['POST'])
def get_price_history_every_minute():
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    # Check if 'hashValue' exists in the session
    hash_value = session.get('hashValue')
    if not hash_value:
        return jsonify({'message': 'No account selected', 'price_history_data': None}), 200

    # Extract parameters from the request JSON body
    params = request.get_json() or {}
    symbol = params.get('symbol').upper()
    start_datetime_str = params.get('start_datetime')
    end_datetime_str = params.get('end_datetime')
    
    print(f"{ex_path} params: {params}")

    # Convert datetime strings to datetime objects
    try:
        if start_datetime_str:
            params['start_datetime'] = datetime.fromisoformat(start_datetime_str)
        if end_datetime_str:
            params['end_datetime'] = datetime.fromisoformat(end_datetime_str)
    except ValueError as e:
        print(f"{ex_path} Invalid datetime format: {e}")
        return jsonify({'message': 'Invalid datetime format', 'price_history_data': None}), 400


    # Call the service function with the extracted parameters
    try:
        price_history_data = services.pricehistory.get_price_history_every_minute(**params)
        print(f"{ex_path} response data: {price_history_data}")

    except Exception as e:
        print(f"{ex_path} There was an exception: {e}")
        return jsonify({
            'message': 'Failed to retrieve pricehistory information',
            'price_history_data': None
        }), 500

    # Return both data and message
    if price_history_data:
        return jsonify({
            'message': 'Price History retrieved successfully',
            'price_history_data': price_history_data
        }), 200
    else:
        return jsonify({
            'message': 'Failed to retrieve pricehistory information',
            'price_history_data': None
        }), 500
