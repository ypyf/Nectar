# coding=utf-8
"""主视图"""

from flask import Blueprint
main = Blueprint('main', __name__)

# 这些语句放在最底部，避免循环导入
from . import views, errors
