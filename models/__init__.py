from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .users import *  # noqa
from .games import *  # noqa


def init_db(app):
    local_database_path = 'database.db'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{local_database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    db.init_app(app)

    with app.app_context():
        db.create_all()
