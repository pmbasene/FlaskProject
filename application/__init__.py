from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin 
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'a0cc3a3a97d7591686b822198050e946'
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'      # theme


# app.config.from_pyfile('myConfig.cfg') # le fichier dans le niveau que celui du __init.py
app.config.from_object('myConfig.DevelopmentConfig')
# app.config.from_object('myConfig.ProductionConfig')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'is-info'

admin_manager = Admin(app, name='BabAdmin')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


from application import views  # to avoid circular import 