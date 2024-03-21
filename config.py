import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'WkmpPFr+Sw9Nz5:6EM3;Zq'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
    SQLALCHEMY_BINDS = {'default':'sqlite:///' + os.path.join(basedir,'data.sqlite')}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SSL_REDIRECT = False
    MAIL_SERVER = 'us2.smtp.mailhostbox.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[TigersolvCRM]'
    FLASKY_MAIL_SENDER = 'Tigersolv CRM <charlton@ballincoder.tech>'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'data.sqlite')
    if os.environ.get('DATABASE_URL')is not None and 'postgres' in os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres','postgresql')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls,app):
        ProductionConfig.init_app(app)
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

    SSL_REDIRECT = True if os.environ.get('DYNO') else False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig
}