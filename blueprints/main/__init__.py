from flask import Blueprint

main = Blueprint('main', __name__)

# noinspection PyPep8
from . import views
