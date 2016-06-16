# coding=utf-8

from threading import Thread
from flask import render_template
from flask_mail import Mail, Message
from flask import current_app
from . import mail

def send_async_email(msg):
    with current_app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    """发送电子邮件"""
    msg = Message(current_app.config['NECTAR_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=current_app.config['NECTAR_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    #msg.html = render_template(template + '.html', **kwargs)
    #thread = Thread(target=send_async_email, args=[msg])
    #thread.start()
    mail.send(msg)
    #return thread
