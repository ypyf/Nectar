# coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from . import auth
from nectar import db
from nectar.email import send_email
from nectar.models import User
from forms import LoginForm, RegisterationForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.home'))
    flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit() # 不提交无法生成userid
        token = user.generate_confirmation_token()
        send_email(user.email, u'请激活您的账号', 'auth/email/confirm',
                   user=user, token=token)
        flash(u'一封账号确认邮件已经发送到您提供的邮箱.')
        return redirect(url_for('main.home'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    if current_user.confirm(token):
        flash(u'您的账号已经成功确认！')
    else:
        flash('该链接无效或超时!')
    return redirect(url_for('main.home'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed  \
        and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.home')
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, u'请激活您的账号', 'auth/email/confirm',
               user=current_user, token=token)
    flash(u'一封账号确认邮件已经发送到您提供的邮箱.')
    return redirect(url_for('main.home'))
