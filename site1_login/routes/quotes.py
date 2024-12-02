from flask import Blueprint, jsonify, request, render_template, g
import services.quotes

quotes_bp = Blueprint('quotes', __name__)

# Route to serve the quotes page
@quotes_bp.route('/quotes', methods=['GET'])
def quotes_page():
    return render_template('quotes/quotes.html', base_template=g.base_template, login_link_url=g.authorization_url, title="Quotes")

# AJAX handler for single symbol quote
@quotes_bp.route('/get_quote', methods=['POST'])
def get_quote():
    data = request.get_json()  # Get JSON payload
    input_text = data.get('input', "").upper()
    result = services.quotes.get_quote(input_text) if input_text else None
    return jsonify({'result': result, 'input': input_text})  # Return JSON response

# AJAX handler for multiple symbols
@quotes_bp.route('/get_quotes', methods=['POST'])
def get_quotes():
    data = request.get_json()  # Get JSON payload
    input_text = data.get('input', "").upper()
    result = services.quotes.get_quotes(input_text) if input_text else None
    return jsonify({'result': result, 'input': input_text})  # Return JSON response
