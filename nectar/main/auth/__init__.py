# coding=utf-8
"""授权视图"""

from flask import Blueprint
auth = Blueprint('auth', __name__)

from . import views


