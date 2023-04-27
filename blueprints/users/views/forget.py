import os

from flask_login import login_required, login_user, logout_user, current_user
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import render_template, request, redirect, url_for

from functools import wraps
from models import User, PermissionPredicate

from .. import users, login_manager

__all__ = []


@users.route('/forget', methods=['GET'])
def forget():
    message = request.args.get('message')
    return render_template('users/forget.html', message=message)


@users.route('/forget-post', methods=['GET', 'POST'])
def forget_post():
    raise NotImplementedError()

    uid = request.form.get('uid')
    pw = request.form.get('pw')

    user = User.get_user_by_cert_pair(uid, pw)
    if user is None:
        return redirect(url_for('.login', message='Incorrect username or password.'))

    login_user(user, remember=True)

    next = request.args.get('next') or url_for('index')
    return redirect(next)
