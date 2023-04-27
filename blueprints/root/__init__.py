from flask import Blueprint

root = Blueprint('root', __name__)

# noinspection PyPep8
from flask_login import LoginManager, current_user

login_manager = LoginManager()

# noinspection PyPep8
from . import views
