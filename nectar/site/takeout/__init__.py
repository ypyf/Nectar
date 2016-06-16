# coding=utf-8
"""授权视图"""

from flask import Blueprint
takeout = Blueprint('takeout', __name__)

from . import views
