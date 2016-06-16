# coding=utf-8
"""
Routes and views for the flask application.
"""

from datetime import datetime
from . import main
from flask import render_template, request, redirect, url_for

@main.route('/')
@main.route('/index')
def home():
    return render_template('index.html', 
                           title=u'首页', 
                           current_time=datetime.utcnow())