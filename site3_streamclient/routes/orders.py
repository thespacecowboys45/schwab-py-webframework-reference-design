from flask import Blueprint, render_template, session, jsonify, request, g
import services.orders

orders_bp = Blueprint('orders', __name__)

# Contact Information route
@orders_bp.route('/orders')
def orders():
    return render_template('orders/orders.html', base_template=g.base_template)

@orders_bp.route('/place_order', methods=['POST'])
def place_order():
    data = request.json
    action = data.get('action')
    order_type = data.get('type')
    price = data.get('price')
    quantity = data.get('quantity')
    symbol = data.get('symbol')

    # Perform input validation
    if not symbol:
        return jsonify({"success": False, "message": "Symbol is required."}), 400
    if order_type == 'market' and price is not None:
        return jsonify({"success": False, "message": "Market orders do not require a price."}), 400
    if order_type == 'limit' and price is None:
        return jsonify({"success": False, "message": "Limit orders require a price."}), 400

    # Simulate order placement
    result = services.orders.place_order(symbol)
    return jsonify({"success": True, "message": result})


@orders_bp.route('/get_orders_for_account', methods=['POST'])
def get_orders_for_account():
    print(f"get_orders_for_account [ entry ]")

    # Check if 'hashValue' exists in the session
    hash_value = session.get('hashValue')
    if not hash_value:
        return jsonify({'message': 'No account selected', 'order_data': None}), 200

    # Extract parameters from the request JSON body
    params = request.get_json() or {}
    max_results = params.get('max_results')
    from_entered_datetime = params.get('from_entered_datetime')
    to_entered_datetime = params.get('to_entered_datetime')
    status = params.get('status')

    print(f"Received params: max_results={max_results}, from_entered_datetime={from_entered_datetime}, "
          f"to_entered_datetime={to_entered_datetime}, status={status}")

    # Call the service function with the extracted parameters
    order_data = services.orders.get_orders_for_account(
        hash_value,
        max_results=max_results,
        from_entered_datetime=from_entered_datetime,
        to_entered_datetime=to_entered_datetime,
        status=status
    )


    # Return both data and message
    if order_data:
        return jsonify({
            'message': 'Order information retrieved successfully',
            'order_data': order_data
        }), 200
    else:
        return jsonify({
            'message': 'Failed to retrieve order information',
            'order_data': None
        }), 500


@orders_bp.route('/get_orders_for_all_linked_accounts', methods=['POST'])
def get_orders_for_all_linked_accounts():
    print(f"get_orders_for_all_linked_accounts [ entry ]")

    # Extract parameters from the request JSON body
    params = request.get_json() or {}
    max_results = params.get('max_results')
    from_entered_datetime = params.get('from_entered_datetime')
    to_entered_datetime = params.get('to_entered_datetime')
    status = params.get('status')

    print(f"Received params: max_results={max_results}, from_entered_datetime={from_entered_datetime}, "
          f"to_entered_datetime={to_entered_datetime}, status={status}")

    # Call the service function with the extracted parameters
    order_data = services.orders.get_orders_for_all_linked_accounts(
        max_results=max_results,
        from_entered_datetime=from_entered_datetime,
        to_entered_datetime=to_entered_datetime,
        status=status
    )

    # Return both data and message
    if order_data:
        return jsonify({
            'message': 'Order information retrieved successfully',
            'order_data': order_data
        }), 200
    else:
        return jsonify({
            'message': 'Failed to retrieve order information',
            'order_data': None
        }), 500
