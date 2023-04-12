import os

from flask_login import login_required, login_user, logout_user, current_user
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import render_template, request, redirect, url_for

from functools import wraps
from models import User

from . import users, login_manager


def check_confirmed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_confirmed:
            return redirect(url_for("users.inactive"))
        return func(*args, **kwargs)

    return wrapper


def check_permission(predicate):
    def decorator(func):
        # TODO: here
        # predicate =
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.check_permission()

        return wrapper

    return decorator


@users.route('/inactive', methods=['GET'])
def inactive():
    return render_template('users/inactive.html')


@users.route('/resend', methods=['GET'])
@login_required
def resend():
    result = update_and_send_verification_token(current_user)

    return render_template('users/resend.html', result=result)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


@users.route('/settings', methods=['GET'])
@login_required
def settings():
    return render_template('users/settings.html')


@users.route('/login', methods=['GET'])
def login():
    message = request.args.get('message')
    return render_template('users/login.html', message=message)


@users.route('/login-post', methods=['GET', 'POST'])
def login_post():
    uid = request.form.get('uid')
    pw = request.form.get('pw')

    user = User.get_user_by_cert_pair(uid, pw)
    if user is None:
        return redirect(url_for('.login', message='Incorrect username or password.'))

    login_user(user, remember=True)

    next = request.args.get('next') or url_for('.index')
    return redirect(next)


def update_and_send_verification_token(user: User):
    token = user.update_verification_token()
    if token is None:
        return False

    url = f'http://192.168.3.15:5000/users/verify/{token}'
    content = f'Verify your email address: {url}'
    print(content)

    return True


@users.route('/verify/<token>', methods=['GET'])
def verify(token):
    verification_result = current_user.verify_token(token)
    return render_template('users/verify.html', result=verification_result)


@users.route('/create', methods=['GET'])
def create():
    return render_template('users/create.html')


@users.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('.login'))


@users.route('/create', methods=['POST'])
def create_post():
    user = User.register(
        name=request.form.get('uid'),
        mail=request.form.get('mail'),
        pw=request.form.get('pw')
    )

    if user is None:
        return redirect('.', message='Failed to create account.')

    update_and_send_verification_token(user)

    return redirect('./create-done')


@users.route('/create-done', methods=['GET'])
def create_done():
    return render_template('users/create-done.html')


@users.route('/')
@login_required
@check_confirmed
def index():
    return render_template(
        'users/index.html'
    )
