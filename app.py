from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm , LoginForm
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a0cc3a3a97d7591686b822198050e946'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default = "default.pjg")
    post = db.relationship('Post', backref='author', lazy = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}',  '{self.image_file}' )"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False )
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow  )
    content = db.Column(db.Text, nullable=False )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

posts = [
            {
                'id': 1,
                'title':'Le savoir', 
                'author':'Papa mamadou sene',
                'content':'Incididunt officia adipisicing nisi ad veniam sunt qui. \
                            Duis enim ea Lorem labore aute. Dolore laboris Lorem do .\
                            Nisi duis adipisicing do exercitation occaecat cupidatat.Veniam ipsum excepteur magna tempor qui labore qui reprehenderit magna dolore aute. Ullamco laboris et cupidatat do ut cillum ex ex cillum reprehenderit adipisicing. Reprehenderit magna eiusmod elit reprehenderit irure fugiat laborum do mollit excepteur. Lorem sit aliquip cillum fugiat enim incididunt ipsum enim tempor elit deserunt veniam.',
                'date_posted':'10-04-2020'
                
            },
            {
                'id': 2,
                'title':'La Sagesse Erudits', 
                'author':'Samba Fall',
                'content':'Deserunt sunt consectetur aliqua incididunt ea enim tempor\
                           cupidatat non in qui tempor. Cillum pariatur labore nisi veniam.\
                           In aliquip consequat fugiat enim minim consectetur et. Voluptate velit amet deserunt id consequat. Fugiat id elit incididunt Lorem commodo velit ex occaecat. Nisi aute elit adipisicing nostrud excepteur eu sit ipsum qui. Commodo laborum cillum velit ut culpa. Ut incididunt velit eiusmod duis Lorem eu laborum aliquip.',
                'date_posted':'12-04-2020'    
            },
            {
                'id': 3,
                'title':'Alchimie', 
                'author':'Papi Kane',
                'content':'Deserunt sunt consectetur aliqua incididunt ea enim tempor\
                           cupidatat non in qui tempor. Cillum pariatur labore nisi veniam.\
                           In aliquip consequat fugiat enim minim consectetur et.Consectetur cupidatat magna est esse. Dolore aliquip consequat id commodo duis cillum aliquip nisi exercitation nostrud adipisicing sit. Pariatur nisi irure est amet incididunt officia nulla amet velit sint pariatur aliqua amet. Occaecat exercitation excepteur Lorem dolore.',
                'date_posted':'13-04-2020'    
            }
        ]

@app.route('/')
@app.route('/home')
def home():
    return render_template('pages/home.html', posts=posts)

@app.route('/contact')
def contact():
    return render_template('pages/contact.html', posts=posts)

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/blog/')
def blog():
    return render_template('pages/blogs/post_index.html',  posts=posts, title='post')

@app.route('/blog/posts/<int:id>')
def blog_show(id):
    post = posts[id - 1] 
    return render_template('pages/blogs/post_show.html', post=post, title='article' )

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html'), 404


# @app.route('/register', methods=['GET','POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():  # envoyer un message flash de succes et retour a la page d'accueil
#         flash(f'Account created for {form.username.data}!', 'is-success')
#         return redirect(url_for('home'))
#     return render_template('register.html', title = 'Register' , form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if request.method =='POST' and form.validate_on_submit():   #and form.validate()  # envoyer un message flash de succes et retour a la page d'accueil
        flash(f'Account created for {form.username.data}!', 'is-success')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register' , form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title = 'login' , form=form)

if __name__ == '__main__':
    app.run(debug=True)


