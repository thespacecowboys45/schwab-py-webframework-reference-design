from flask import Blueprint

#from .schwab import schwab_bp
from .accounts import accounts_bp
from .quotes import quotes_bp
#from .pricehistory import pricehistory_bp
#from .search_and_fundamentals import search_and_fundamentals_bp
#from .transactions import transactions_bp
#from .positions import positions_bp
#from .trade import trade_bp
#from .orders import orders_bp
from .website_navigation import website_navigation_bp
#from .development_tools import development_tools_bp
#from .celery_app import celery_bp

# remove this for reference design
#from .automations import automations_bp

def register_routes(app):
    #app.register_blueprint(schwab_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(quotes_bp)
    #app.register_blueprint(pricehistory_bp)
    #app.register_blueprint(search_and_fundamentals_bp)
    #app.register_blueprint(transactions_bp)
    #app.register_blueprint(positions_bp)
    #app.register_blueprint(trade_bp)
    #app.register_blueprint(orders_bp)
    app.register_blueprint(website_navigation_bp)
    ##app.register_blueprint(development_tools_bp)
    #app.register_blueprint(celery_bp)

    # remove this for reference design
    #app.register_blueprint(automations_bp)
    

