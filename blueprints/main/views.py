from flask import *

from flask_login import login_required

from . import main


@main.route('/')
def index():
    return render_template('main/index.html')
