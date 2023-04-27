from flask import Blueprint

marton = Blueprint('marton', __name__)

# noinspection PyPep8
from . import views
