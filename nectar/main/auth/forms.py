# coding=utf-8

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from nectar.models import User

class LoginForm(Form):
    email = StringField(u'电子邮件', validators=[Required(), Length(1, 64), Email(u'无效的电子邮件地址')])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'保持登录')
    submit = SubmitField(u'登录')

class RegisterationForm(Form):
    email = StringField(u'电子邮件', validators=[Required(), Length(1, 64), Email(u'无效的电子邮件地址')])
    username = StringField(u'用户名称', validators=[Required(), Length(1, 64),
                           Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户们必须是字母、数字、点或者下划线')])
    password = PasswordField(u'密码', validators=[Required(),
                             EqualTo('password2', message=u'两次输入的密码不匹配.')])
    password2 = PasswordField(u'再输入一次密码', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'这个邮件地址已经被使用.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'这个用户名已经被使用.')
