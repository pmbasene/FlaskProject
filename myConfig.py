import os

class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    USER_RELOADER=True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587     # 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


    

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = 'a0cc3a3a97d7591686b822198050e946'
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db" 
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_ADMIN_SWATCH = 'cerulean'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'babaguedj@gmail.com'
    MAIL_PASSWORD = 'babaguedj12&'
