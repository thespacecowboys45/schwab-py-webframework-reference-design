from flask import Blueprint

from .accounts import accounts_bp
from .quotes import quotes_bp
from .streaming_quotes import streaming_quotes_bp
from .pricehistory import pricehistory_bp
from .search_and_fundamentals import search_and_fundamentals_bp
from .transactions import transactions_bp
from .positions import positions_bp
from .trade import trade_bp
from .orders import orders_bp
from .celery_examples import celery_examples_bp
from .website_navigation import website_navigation_bp

def register_routes(app):
    app.register_blueprint(accounts_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(streaming_quotes_bp)
    app.register_blueprint(pricehistory_bp)
    app.register_blueprint(search_and_fundamentals_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(positions_bp)
    app.register_blueprint(trade_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(celery_examples_bp)
    app.register_blueprint(website_navigation_bp)    

