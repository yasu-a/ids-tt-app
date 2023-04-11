from flask import *
import os

# create app instance
app = Flask(__name__)

# configure app
app.config['SECRET_KEY'] = 'mysite'
app.config['SQLALCHEMY_DATABASE_URI'] \
    = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__name__)), 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# register blueprints
from blueprints.main import main
from blueprints.users import users

app.register_blueprint(main, url_prefix='/main')
app.register_blueprint(users, url_prefix='/users')

# initialize db
from models import db

db.init_app(app)
with app.app_context():
    db.create_all()

# initialize login manager
from blueprints.users import login_manager

login_manager.login_view = 'users.login'
login_manager.init_app(app)


@app.route('/')
def hello():
    return redirect(url_for('main.index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
