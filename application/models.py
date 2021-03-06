from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app , redirect
from datetime import datetime
from application import db, login_manager, admin_manager 
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default ="default.jpg")
    is_admin = db.Column(db.Boolean, default=False)
    post = db.relationship('Post', backref='author', lazy = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}',  '{self.image_file}' )"

    def get_reset_token(self, expire_sec= 1800):
        s= Serializer(current_app.config['SECRET_KEY'], expire_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s= Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
        


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False )
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow  )
    content = db.Column(db.Text, nullable=False )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"Post('{self.title}', '{self.content}', '{self.date_posted}')"



# model pour les tests

class Editor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    html = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(20), nullable=True)


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=True, default = datetime.utcnow ) # afin quelle soit facultative
    # image_file = db.Column(db.String(20), nullable=True, default ="default.jpg")
    
    

#https: // flask-user.readthedocs.io/en/latest/data_models.html#roleanduserroledatamodels
# Admin Model
class ControllerAdmin(ModelView):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)

    def is_accessible(self):
        return current_user.is_authenticated

    def is_not_accessible(self):
        # return "You are not authorized to access admin dashboard"
        return redirect(url_for('users.login', next=request.url))

admin_manager.add_view(ControllerAdmin(User, db.session))
admin_manager.add_view(ControllerAdmin(Post, db.session))
admin_manager.add_view(ControllerAdmin(Editor, db.session))
admin_manager.add_view(ControllerAdmin(Weather, db.session))
        
