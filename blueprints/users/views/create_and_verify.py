import os

from flask_login import login_required, login_user, logout_user, current_user
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import render_template, request, redirect, url_for

from functools import wraps
from models import User, PermissionPredicate

from .. import users, login_manager

import urllib.parse

__all__ = []


@users.route('/inactive', methods=['GET'])
def inactive():
    return render_template('users/inactive.html')


@users.route('/resend', methods=['GET'])
@login_required
def resend():
    result = update_and_send_verification_token(current_user)

    return render_template('users/resend.html', result=result)


@users.route('/verify/<token>', methods=['GET'])
@login_required
def verify(token):
    verification_result = current_user.verify_token(token)
    return render_template('users/verify.html', result=verification_result)


def update_and_send_verification_token(user: User):
    token = user.update_verification_token()
    if token is None:
        return False

    url = urllib.parse.urljoin(request.url, f'/users/verify/{token}')
    content = f'Verify your email address: {url}'

    print(content)

    return True


@users.route('/create', methods=['GET'])
def create():
    message = request.args.get('message')
    return render_template('users/create.html', message=message)


@users.route('/create', methods=['POST'])
def create_post():
    user = User.register(
        name=request.form.get('uid'),
        mail=request.form.get('mail'),
        pw=request.form.get('pw')
    )

    if user is None:
        return redirect(url_for('.create', message='Failed to create account.'))

    update_and_send_verification_token(user)
    login_user(user)

    return redirect('./create-done')


@users.route('/create-done', methods=['GET'])
def create_done():
    return render_template('users/create-done.html')
