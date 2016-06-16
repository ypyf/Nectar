# coding=utf-8
"""应用程序配置"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'why would I tell you my secret key?'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #NECTAR_MAIL_SUBJECT_PREFIX = '[Nectar]'
    #NECTAR_MAIL_SENDER = 'Nectar Admin <t34@qq.com>'
    #NECTAR_ADMIN = os.environ.get('NECTAR_ADMIN') or 'admin'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    NECTAR_MAIL_SUBJECT_PREFIX = u'[Nectar 企业版]'
    NECTAR_MAIL_SENDER = u'Nectar 管理员 <t34@qq.com>'
    MAIL_SERVER = 'smtp.qq.com'   # 可以替换成本地的SMTP服务器
    MAIL_USE_SSL = True           # 使用QQ邮件服务器必选
    MAIL_PORT = 465               # QQ SMTP服务器断开
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '12345')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '12345')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db/nectar-dev.db')
    print SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        from datetime import datetime
        app.jinja_env.globals['year'] = datetime.now().year

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db/nectar-test.db')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db/nectar.db')

# 不同版本的配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
