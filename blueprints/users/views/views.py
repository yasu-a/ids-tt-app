import os

from flask_login import login_required, login_user, logout_user, current_user
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import render_template, request, redirect, url_for

from functools import wraps
from models import User, PermissionPredicate

from .. import users, login_manager

from . import check_permission, check_confirmed

__all__ = []


@users.route('/settings', methods=['GET'])
@check_confirmed
def settings():
    nav_root = current_user.check_permission('root')
    return render_template('users/settings.html', nav_root=nav_root)


@users.route('/')
def index():
    return render_template(url_for('users.settings'))
