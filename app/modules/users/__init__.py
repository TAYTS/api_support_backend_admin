from flask import Blueprint

# Import all the view function
from app.modules.users.login import login
from app.modules.users.register import register

# Define the blueprint name
module = Blueprint('users', __name__)

module.add_url_rule('/users/login',
                    view_func=login, methods=['POST'])
module.add_url_rule('/users/register',
                    view_func=register, methods=['POST'])
