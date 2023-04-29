from . import db


class ModelBase(db.Model):
    __abstract__ = True
