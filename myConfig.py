class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'a0cc3a3a97d7591686b822198050e946'
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = 'a0cc3a3a97d7591686b822198050e946'
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'
