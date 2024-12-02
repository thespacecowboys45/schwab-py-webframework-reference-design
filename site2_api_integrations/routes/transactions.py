from flask import Blueprint, render_template, session, jsonify, request, g
import services.transactions

transactions_bp = Blueprint('transactions', __name__)

# Contact Information route
@transactions_bp.route('/transactions')
def transactions():
    return render_template('transactions/transactions.html', base_template=g.base_template)


@transactions_bp.route('/get_transactions', methods=['POST'])
def get_transactions():
    print(f"get_transactions [ entry ]")

    # Check if 'hashValue' exists in the session
    hash_value = session.get('hashValue')
    if not hash_value:
        return jsonify({'message': 'No account selected', 'transaction_data': None}), 200

    # Extract parameters from the request JSON body
    params = request.get_json() or {}
    start_date = params.get('start_date')
    end_date = params.get('end_date')
    transaction_type = params.get('transaction_type')
    symbol = params.get('symbol')


    print(f"Received params: start_date={start_date}, end_date={end_date}, "
          f"transaction_type={transaction_type}, symbol={symbol}")

    # Call the service function with the extracted parameters
    transaction_data = services.transactions.get_transactions(
        hash_value,
        start_date=start_date,
        end_date=end_date,
        transaction_type=transaction_type,
        symbol=symbol
    )

    # Return both data and message
    if transaction_data:
        return jsonify({
            'message': 'Transaction information retrieved successfully',
            'transaction_data': transaction_data
        }), 200
    else:
        return jsonify({
            'message': 'Failed to retrieve transaction information',
            'transaction_data': None
        }), 500
