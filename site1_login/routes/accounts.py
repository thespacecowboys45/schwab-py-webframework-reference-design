from flask import Blueprint, render_template, request, session, jsonify, g
import services.accounts
import inspect

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/accounts')
def accounts():
    return render_template('accounts/accounts.html', base_template=g.base_template, login_link_url=g.authorization_url, title="Accounts")

# Route to retrieve account information
@accounts_bp.route('/get_account', methods=['GET'])
def get_account():
    # Check if 'hashValue' exists in the session
    hash_value = session.get('hashValue')

    if not hash_value:
        return jsonify({'message': 'No account selected'}), 200

    print(f"services.accounts.get_account [ hash_value : {hash_value} ]")

    # If hashValue exists, call get_account() with hashValue
    account_data = services.accounts.get_account(hash_value)

    # Return both account data and message
    if account_data:
        return jsonify({
            'message': 'Account information retrieved successfully',
            'account_data': account_data
        }), 200
    else:
        return jsonify({
            'message': 'Failed to retrieve account information',
            'account_data': None
        }), 500

@accounts_bp.route('/get_account_numbers', methods=['GET'])
def get_account_numbers():
    response = services.accounts.get_account_numbers()
    return jsonify(response)    


@accounts_bp.route('/select_account', methods=['POST'])
def select_account():
    data = request.get_json()
    account_number = data.get('accountNumber')
    hash_value = data.get('hashValue')

    if account_number and hash_value:
        session['accountNumber'] = account_number
        session['hashValue'] = hash_value
        return jsonify({"message": "Account selected successfully"})
    return jsonify({"message": "Invalid account data"}), 400

@accounts_bp.route('/clear_account_selection', methods=['POST'])
def clear_account_selection():
    session.pop('accountNumber', None)
    session.pop('hashValue', None)
    return jsonify({"message": "Account selection cleared"})

@accounts_bp.route('/get_accounts', methods=['GET'])
def get_accounts():
    response = services.accounts.get_accounts()
    return jsonify(response)    

@accounts_bp.route('/get_user_preferences', methods=['POST'])
def get_user_preferences():
    print(f"{__name__} [ entry ]")

    response = services.accounts.get_user_preferences()
    return jsonify(response)    


@accounts_bp.route('/get_positions', methods=['POST'])
def get_positions():
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    # Check if 'hashValue' exists in the session
    hash_value = session.get('hashValue')

    if not hash_value:
        return jsonify({'message': 'No account selected'}), 200    

    response = services.accounts.get_positions(hash_value)
    return jsonify(response)    
