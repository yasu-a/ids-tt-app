import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import render_template, request, redirect, url_for

import models

from . import users

@flask_login.user_g

@users.route('/')
def index():
    return render_template(
        'main/index.html'
    )
