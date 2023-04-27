from flask import Blueprint

users = Blueprint('users', __name__)

# noinspection PyPep8
from flask_login import LoginManager, current_user

login_manager = LoginManager()

# noinspection PyPep8
from . import views

check_confirmed = views.check_confirmed
