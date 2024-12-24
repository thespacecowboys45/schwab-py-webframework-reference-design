from flask import Blueprint, jsonify, request, render_template, g
import services.search_and_fundamentals
from datetime import datetime


#search_and_fundamentals_bp = Blueprint('search_and_fundamentals', __name__, url_prefix="search_and_fundamentals")
search_and_fundamentals_bp = Blueprint('search_and_fundamentals', __name__)

@search_and_fundamentals_bp.route('/search_and_fundamentals')
def search_and_fundamentals():
    return render_template('search_and_fundamentals/search_and_fundamentals.html', base_template=g.base_template)

@search_and_fundamentals_bp.route('/get_instruments', methods=['POST'])
def get_instruments():
    print(f"{__name__} [ entry ]")
    data = request.get_json()  # Get JSON payload

    symbol = data.get('symbol', "").upper()
    projection = data.get('projection', "").upper()

    result = services.search_and_fundamentals.get_instruments(symbol, projection) if symbol else None
    return jsonify({'result': result, 'input': data})  # Return JSON response

@search_and_fundamentals_bp.route('/movers')
def movers():
    print(f"{__name__} [ entry ]")

    return render_template('search_and_fundamentals/movers.html', base_template=g.base_template)


@search_and_fundamentals_bp.route('/get_movers', methods=['POST'])
def get_movers():
    print(f"{__name__} [ entry ]")

    data = request.get_json() or {} # Get JSON payload

    index = data.get('index', "").upper()
    sortorder = data.get('sortorder', "").upper()    
    frequency = data.get('frequency', "").upper()    

    result = services.search_and_fundamentals.get_movers(index, sortorder, frequency)
    return jsonify({'result': result, 'input': data})  # Return JSON response

@search_and_fundamentals_bp.route('/market_hours')
def market_hours():
    return render_template('search_and_fundamentals/market_hours.html', base_template=g.base_template)


@search_and_fundamentals_bp.route('/get_market_hours', methods=['POST'])
def get_market_hours():    
    print(f"{__name__} [ entry ]")

    data = request.get_json() or {} # Get JSON payload

    market = data.get('market', "").upper()
    date_str = data.get('date', "")

    # Convert datetime strings to datetime objects
    try:
        if date_str:
            data['date'] = datetime.fromisoformat(date_str)
        else:
            data['date'] = None
    except ValueError as e:
        print(f"{ex_path} Invalid datetime format: {e}")
        return jsonify({'message': 'Invalid datetime format', 'market_hours_data': None}), 400


    result = services.search_and_fundamentals.get_market_hours(**data)
    return jsonify({'result': result, 'input': data})  # Return JSON response