from flask import Blueprint, render_template, jsonify, g, session
import os
import inspect

website_navigation_bp = Blueprint('website_navigation', __name__)

# Contact Information route
@website_navigation_bp.route('/contact')
def contact():
    content = "Contact us at: example@example.com"
    return render_template('website_navigation/contact.html', base_template=g.base_template, login_link_url=g.authorization_url)


# Documentation route
@website_navigation_bp.route('/documentation')
def documentation():
    content = "This is the documentation page. Here you'll find information on how to use this website."
    return render_template('website_navigation/documentation.html', base_template=g.base_template, login_link_url=g.authorization_url)

@website_navigation_bp.route('/logout')
def logout():
    # for dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    if g.token_path:
        # IF we had selected an account to use, unselect it
        session.pop('accountNumber', None)
        session.pop('hashValue', None)

        if os.path.exists(g.token_path):
            os.remove(g.token_path)
            message = f"You have been logged out. {g.token_path} removed from system."
        else:
            message = f"You were not logged in to begin with!"
    else:
        message = f"No token_path is set.  You must set a token_path."

    return render_template('website_navigation/logout.html', base_template=g.base_template, login_link_url=g.authorization_url, message=message)    
