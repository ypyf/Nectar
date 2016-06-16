# coding=utf-8
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from . import main


@main.route('/')
@main.route('/index')
def home():
    if current_user.is_authenticated:
        return render_template('index.html', title=u'首页',
                               current_time=datetime.utcnow())
    return redirect(request.args.get('next') or url_for('auth.login'))
