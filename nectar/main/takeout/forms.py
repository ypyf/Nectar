# coding=utf-8

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from nectar.models import User


class WifiQueryForm(Form):
    ssid = StringField(u'SSID', validators=[Required(), Length(1, 64),
                       Email(u'无效的电子邮件地址')])
    submit = SubmitField(u'查询')
