from flask import Blueprint, render_template, request, current_app, session, g
import os
import logging
import inspect
import json

import services.trade

from schwab.orders.equities import equity_buy_market, equity_buy_limit
from schwab.orders.equities import equity_sell_market, equity_sell_limit



trade_bp = Blueprint('trade', __name__,  url_prefix='/trade')

# Contact Information route
@trade_bp.route('/trade')
def trade():
    return render_template('trade/trade.html', base_template=g.base_template, symbol='AAPL', quantity='1')

@trade_bp.route('/buy', methods=['POST'])
def buy():
    logging.debug(f"trade.py [ buy ] [ entry ]")

    return "bought"

@trade_bp.route('/sell', methods=['POST'])
def sell():
    logging.debug(f"trade.py [ sell ] [ entry ]")    

    return "sold"


@trade_bp.route('/place_order', methods=['POST'])
def place_order():
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    #print(f"{ex_path} [ entry ]")
    logging.info(f"{ex_path} [ entry ]")    


    # Check if 'hashValue' exists in the session
    hash_value = session.get('hashValue')
    if not hash_value:
        return jsonify({'message': 'No account selected', 'order_data': None}), 200    

    data = request.get_json()  # Get JSON payload
    current_app.logger.info(f"{ex_path} data: {data}")

    order = create_order_json(**data)

    current_app.logger.info(f"{ex_path} order: {order}")

    result = services.trade.place_order(hash_value, order)

    print(f"RESULT OF services.trace.place_order: {result}")
    

    return json.dumps({"message":"order_placed", "result": result})


# uses schwab-py helper functions
def create_order_json(symbol, quantity, price, orderType, instruction):
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    # Cast quantity as int.  It's a string, coming from the browser request
    quantity = int(quantity)

    # Determine the action based on instruction and orderType
    if instruction.upper() == "BUY":
        if orderType.upper() == "MARKET":
            return equity_buy_market(symbol, quantity)
        elif orderType.upper() == "LIMIT":
            return equity_buy_limit(symbol, quantity, price)
        else:
            raise ValueError("Invalid orderType: must be 'market' or 'limit'")        

    elif instruction.upper() == "SELL":
        if orderType.upper() == "MARKET":
            return equity_sell_market(symbol, quantity)
        elif orderType.upper() == "LIMIT":
            return equity_sell_limit(symbol, quantity, price)
        else:
            raise ValueError("Invalid orderType: must be 'market' or 'limit'")        



def create_order_json_manually(symbol, quantity, price, orderType, instruction):
    # Determine the action based on instruction and orderType
    if instruction.upper() == "BUY":
        action = "BUY" if orderType == "MARKET" else "BUY_TO_OPEN"
    elif instruction.upper() == "SELL":
        action = "SELL" if orderType == "MARKET" else "SELL_TO_OPEN"
    else:
        raise ValueError("Invalid instruction: must be 'buy' or 'sell'")

    # Create the base structure for the order
    order = {
        "orderType": orderType.upper(),
        "session": "NORMAL",
        "duration": "DAY",
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
                #"instruction": action,
                "instruction": instruction.upper(),
                "quantity": int(quantity),
                "instrument": {
                    "symbol": symbol,
                    "assetType": "EQUITY"
                }
            }
        ]
    }

    # Add the price if the order type is LIMIT
    if orderType.upper() == "LIMIT":
        order["price"] = str(price)

    # Return the order as a JSON string
    return json.dumps(order, indent=2)


