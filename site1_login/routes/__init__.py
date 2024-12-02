from flask import Blueprint

from .accounts import accounts_bp
from .quotes import quotes_bp
from .website_navigation import website_navigation_bp

def register_routes(app):
    app.register_blueprint(accounts_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(website_navigation_bp)    

