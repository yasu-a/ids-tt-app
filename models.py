import contextlib
import re

from flask_sqlalchemy import SQLAlchemy
import datetime
import dateutil.parser
import flask_login
import secrets

import argon2

db = SQLAlchemy()


class ModelBase(db.Model):
    __abstract__ = True


def normalize_date(date):
    if isinstance(date, str):
        date = dateutil.parser.parse(date)
    if not isinstance(date, datetime.date):
        raise TypeError('invalid type of arg')
    return date


class UserVerificationToken(db.Model):
    __tablename__ = 'user_verif'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    token = db.Column(db.String)
    verified = db.Column(db.Boolean)

    def __init__(self, user_id, token):
        self.id = user_id
        self.token = token
        self.verified = False

    @classmethod
    def __exists_for_user(cls, user_id):
        entry_exists = db.session.query(
            cls.query.filter(
                cls.id == user_id
            ).exists()
        ).scalar()

        return bool(entry_exists)

    @classmethod
    def get_for_user(cls, user_id):
        entry = cls.query.filter(
            cls.id == user_id
        ).first()

        return entry

    @classmethod
    def is_verified_user(cls, user_id):
        entry = cls.get_for_user(user_id)
        if entry is None:
            return False
        return entry.verified

    @classmethod
    def update_for_user(cls, user_id):
        new_token = secrets.token_hex(64)

        if not cls.__exists_for_user(user_id):
            entry = cls(user_id, new_token)
            db.session.add(entry)
        else:
            entry = cls.get_for_user(user_id)
            if entry.verified:
                return None
            entry.token = new_token

        db.session.commit()

        return new_token

    @classmethod
    def set_verified_for_user(cls, user_id):
        entry = cls.get_for_user(user_id)
        if entry is not None:
            entry.verified = True
            db.session.commit()


class NameSetColumnWrapper:
    def __init__(self, entry, attr_name):
        self.__entry = entry
        self.__attr_name = attr_name

    @contextlib.contextmanager
    def name_set(self):
        value = getattr(self.__entry, self.__attr_name)
        items = set(item for item in re.split(r'[+\s]+', value) if item)
        yield items
        new_value = '+'.join(items)
        setattr(self.__entry, self.__attr_name, new_value)

    def __contains__(self, item):
        with self.name_set() as s:
            return item in s

    def add(self, item):
        with self.name_set() as s:
            s.add(item)

    def delete(self, item):
        with self.name_set() as s:
            s.remove(item)


class User(ModelBase, flask_login.UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    mail = db.Column(db.String)
    pw_hash = db.Column(db.LargeBinary)

    permission = db.Column(db.String)

    # verification_token = db.relationship('UserVerificationToken', backref='user', lazy='joined')

    PASSWORD_ENCODING = 'latin-1'

    @property
    def is_confirmed(self):
        return UserVerificationToken.is_verified_user(self.id)

    def verify_token(self, token):
        entry = UserVerificationToken.get_for_user(self.id)
        if entry is None:
            return False

        if entry.token == token:
            UserVerificationToken.set_verified_for_user(self.id)
            return True

        return False

    @classmethod
    def get_user_by_cert_pair(cls, name, pw):
        user = cls.query.filter(
            db.and_(
                User.name == name
            )
        ).first()

        print(user)

        if user:
            try:
                argon2.verify_password(
                    user.pw_hash,
                    pw.encode(cls.PASSWORD_ENCODING)
                )
            except argon2.exceptions.VerifyMismatchError:
                user = None

        return user

    def update_verification_token(self):
        token = UserVerificationToken.update_for_user(self.id)
        return token

    @classmethod
    def register(cls, name, mail, pw):
        invalid = db.session.query(
            cls.query.filter(
                db.or_(
                    cls.name == name,
                    cls.mail == mail
                )
            ).exists()
        ).scalar()
        if invalid:
            return None

        user = cls()
        user.name = name
        user.mail = mail
        user.pw_hash = argon2.hash_password(pw.encode(cls.PASSWORD_ENCODING))
        user.permission = ''

        db.session.add(user)
        db.session.commit()

        user.update_verification_token()

        return user

    def add_permission(self, name):
        col = NameSetColumnWrapper(self, 'permission')
        col.add(name)

    def check_permission(self, name):
        col = NameSetColumnWrapper(self, 'permission')
        return name in col

    def remove_permission(self, name):
        col = NameSetColumnWrapper(self, 'permission')
        col.delete(name)


class PermissionPredicate:
    def __init__(self, predicate):
        self.__predicate = predicate

    @classmethod
    def from_string(cls, name):
        def predicate(checker):
            return checker(name)

        return cls(predicate)

    def __call__(self, checker):
        return self.__predicate(checker)


class Game(ModelBase):
    __tablename__ = 'game'

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
    local_database_path = 'database.db'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{local_database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    db.init_app(app)

    with app.app_context():
        db.create_all()
