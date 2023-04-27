from flask import *

from flask_login import login_required

from . import root

from models import User


@root.route('/users')
def users():
    context = dict(
        entries=User.query.all(),
        keys=['name', 'mail', 'permission']
    )
    return render_template('root/users.html', **context)


@root.route('/')
def index():
    return redirect(url_for('.users'))
