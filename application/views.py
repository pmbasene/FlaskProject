
from flask import render_template, url_for, flash, redirect, request
from application import app, db , bcrypt
from application.forms import RegistrationForm , LoginForm
from application.models import User, Post

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
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user  = User(username = form.username.data, email=form.email.data , password =  password_hash )
        db.session.add(user)
        db.session.commit()
        flash(f' Welcome you are logged in!', 'is-success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register' , form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title = 'login' , form=form)
