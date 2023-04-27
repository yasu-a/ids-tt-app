import os

from flask_login import login_required, login_user, logout_user, current_user
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import render_template, request, redirect, url_for

from functools import wraps
from models import User, PermissionPredicate

from .. import users, login_manager

__all__ = 'check_confirmed', 'check_permission'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


def check_confirmed(func):
    func = login_required(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_confirmed:
            return redirect(url_for("users.inactive"))
        return func(*args, **kwargs)

    return wrapper


def check_permission(predicate):
    def decorator(func):
        func = check_confirmed(func)

        nonlocal predicate

        predicate = PermissionPredicate.normalize(predicate)

        @wraps(func)
        def wrapper(*args, **kwargs):
            has_permission = predicate(current_user.check_permission)
            if not has_permission:
                return render_template('users/deny.html'), 403
            return func(*args, **kwargs)

        return wrapper

    return decorator
