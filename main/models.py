from flask_sqlalchemy import SQLAlchemy
import datetime
import dateutil.parser

db = SQLAlchemy()


class ModelBase(db.Model):
    __abstract__ = True


def normalize_date(date):
    if isinstance(date, str):
        date = dateutil.parser.parse(date)
    if not isinstance(date, datetime.date):
        raise TypeError('invalid type of arg')
    return date


class Game(ModelBase):
    __tablename__ = 'games'

    def __init__(self, date, name, right_left, content):
        self.date = normalize_date(date)
        self.name = name
        self.right_left = right_left
        self.content = content

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    name = db.Column(db.Text)
    right_left = db.Column(db.Text)
    content = db.Column(db.LargeBinary)


def init_db(app):
    local_database_path = '../database.db'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{local_database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    db.init_app(app)

    with app.app_context():
        db.create_all()
