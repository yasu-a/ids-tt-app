from flask import Blueprint

users = Blueprint('users', __name__)

# noinspection PyPep8
from . import views
