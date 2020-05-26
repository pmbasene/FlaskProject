from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin 
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail

app = Flask(__name__)


# app.config.from_pyfile('myConfig.cfg') # le fichier dans le niveau que celui du __init.py
app.config.from_object('myConfig.DevelopmentConfig')
# app.config.from_object('myConfig.ProductionConfig')

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
admin_manager = Admin() #or Admin(name='BabAdmin')
login_manager.login_message_category = 'is-info'
login_manager.login_view = 'users.login'

# migration extentions
migrate = Migrate(app, db)
manager_migration = Manager(app)
manager_migration.add_command('db', MigrateCommand)




def create_app(config_class= 'myConfig.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object('myConfig.DevelopmentConfig')    # app.config.from_pyfile('myConfig.cfg') # le fichier dans le niveau que celui du __init.py
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin_manager.init_app(app)
    
    from application.users.views import users 
    from application.posts.views import posts 
    from application.main.views import main
    from application.summernote.views import summers
    from application.apiWeather.views import weathers 
    from application.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(weathers)
    app.register_blueprint(summers)
    app.register_blueprint(errors)
    
    return app


            
