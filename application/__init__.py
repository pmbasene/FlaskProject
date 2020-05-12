from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a0cc3a3a97d7591686b822198050e946'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
admin_manager = Admin(app, name='Admin_Baba', template_mode='bootstrap3')

login_manager.login_view = 'login'
login_manager.login_message_category = 'is-info'

from application import views  # to avoid circular import 