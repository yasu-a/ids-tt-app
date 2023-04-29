import datetime

import dateutil.parser

from . import db
from .base import ModelBase


def normalize_date(date):
    if isinstance(date, str):
        date = dateutil.parser.parse(date)
    if not isinstance(date, datetime.date):
        raise TypeError('invalid type of arg')
    return date


class Game(ModelBase):
    __tablename__ = 'game'

    def __init__(self, date, name, content):
        self.date = normalize_date(date)
        self.name = name
        self.content = content

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    name = db.Column(db.Text)
    content = db.Column(db.LargeBinary)
