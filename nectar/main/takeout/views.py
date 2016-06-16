# coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from nectar import db
from nectar.models import User
from nectar import db
from forms import WifiQueryForm
from nectar.template import templated
from . import takeout


@takeout.route('/wifi', methods=['GET', 'POST'])
@templated('takeout/wifi.html')
def wifi():
    form = WifiQueryForm()
    if form.validate_on_submit():
        # TODO 执行查询
        return dict(form=form)
    flash('无效的SSID')
    return dict(form=form)
