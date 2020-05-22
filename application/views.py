import requests
import os
import secrets
from PIL import Image
# from flask_sqlalchemy import sqlalchemy # pour utliser la fonction desc de sqlalchemy . Remarque # from flask_sqlalchemy.sqlalchemy import desc , ne marche pas , why??
from flask import render_template, url_for, flash, redirect, request, abort
from application import app, db , bcrypt
from application.forms import RegistrationForm , LoginForm, UpdateAccountForm, PostFrom
from application.models import User, Post, Editor, Weather
from flask_login import login_user, current_user, logout_user, login_required

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

# filter personnalité tres utile
# @app.template_fliter('date_normale')
# def date_normale(dt):
#     return dt.strftime('%d %b %Y')




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
    page = request.args.get('page', 1, type=int)
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,  per_page=3)
    # post = Post.query.order_by(sqlalchemy.desc(Post.date_posted)).all()    # pour trier du plus recent ...
    return render_template('pages/blogs/post_index.html',  posts=post, title='All Posts')

@app.route('/blog/post/<int:id>')
def blog_show(id):
    # post = posts[int(id) - 1] 
    post = Post.query.get_or_404(id)
    return render_template('pages/blogs/post_show.html', posts=post, title='article' )

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html'), 404

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if request.method =='POST' and form.validate_on_submit():   #and form.validate()  # envoyer un message flash de succes et retour a la page d'accueil
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user  = User(username = form.username.data, email=form.email.data , password =  password_hash )
        db.session.add(user)
        db.session.commit()
        flash(f' Welcome you are registered in!', 'is-success')
        return redirect(url_for('login'))
    return render_template('pages/register.html', title = 'Register' , form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password ,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Good! You have been logged in.', 'is-succes')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessul. Try again! Your credentials is false', 'is-danger')
    return render_template('pages/login.html', title = 'login' , form=form)


@app.route('/admin', methods=['GET','POST'])
def admin():
    form = AdminForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'admin':
            print('youre login !!!')
            redirect(url_for('home'))
    return render_template('admin/index.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ ,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/src/img/profile_pics', picture_fn)

    output_size  = (128, 128)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)


    return picture_fn

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account have been updated', 'is-success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='src/img/profile_pics/' + current_user.image_file)
    return render_template('pages/account.html', title='account', image_file=image_file, form=form)

@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostFrom()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'is-success')
        return redirect(url_for('blog'))
    return render_template('pages/blogs/create_post.html', title='New Post', 
    form=form, legend = "Creer un nouveau Post")

@app.route('/blog/post/<int:id>/update',methods=['GET','POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    form = PostFrom()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(' Your Post has been update!', 'is-success')
        return redirect(url_for('blog_show', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('pages/blogs/create_post.html', title='Update Post', 
           form= form, legend = "Mise à jour du Post" )
 
@app.route('/blog/post/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(' Your Post has been deleted!', 'is-success')
    return redirect(url_for('home'))


# my stuff
@app.route('/testjs')
def testjs():
    return render_template('testjs.html')



# -----route for testing----- 

@app.route('/garage')     # for integrating video format
def garage():
    return render_template('pages/garage.html', title='Garage tools')


@app.route('/summernote', methods=['POST', 'GET'])  # for integrating text editor
def summernote():
    if request.method == 'POST' :
        editor = Editor(html=request.form.get('editordata'))
        # print(request.form.get('editordata'))
        db.session.add(editor)
        db.session.commit()
        # return 'Posted Data'
        return redirect(url_for('display'))
    return render_template('docEssai/summernote.html')


@app.route('/display')   # linked to summernote route , able to display post 
def display():
    posts = Editor.query.all()
    print(posts)
    # return 'data received'
    return render_template('docEssai/display.html', posts=posts)


# @app.route('/display/<int:id>')
# def display(id):
#     posts = Editor.query.get(id)
#     print(posts)
#     # return 'data received'
#     return render_template('docEssai/display.html', posts=posts)






@app.route('/apiWeather', methods=['GET'])
def apiWeather():
    #    # todo
        # add city name in data database for query throught a search bar
        # create column side which contains all regions

    collectData = []
    cities = Weather.query.order_by(Weather.date_posted.desc()).all()
    
    for city in cities:
        resp = get_weather_data(city.name)
        data = { 
            'city'        : city.name ,
            'temp'        : resp['main']['temp'],
            'temp_min'        : resp['main']['temp_min'],
            'temp_max'        : resp['main']['temp_max'],
            'pressure'    : resp['main']['pressure'],
            'humidity'    : resp['main']['humidity'],
            'description' : resp['weather'] [0]['description'] ,
            'icon'        : resp['weather'][0]['icon'] ,
            'wind_speed' :  resp['wind']['speed'],
            # 'wind_deg'    : resp['wind']['deg'],
        }
        collectData.append(data)
    return render_template('docEssai/apiWeather.html',collectData=collectData)
    
@app.route('/apiWeather', methods=['POST'])
def apiWeather_post():
    city = request.form.get('city')
    if city: # check if input , permet d"empecher d'entrer des donnees vides
        check_existing_city = Weather.query.filter_by(name=city).first()
        if not check_existing_city:  # si la ville n'hesite pas deja dans la db. il permet d'eviter la replication
            resp = get_weather_data(city)    # on appelle la fonction renvoie le dataset originel de openweather
            if resp['cod'] == 200:
                weather = Weather(name=city)
                db.session.add(weather)
                db.session.commit()
                flash(f'Good! Les conditions climatiques pour la ville de {city} sont bien disponibles', 'is-success')
            else:
                flash('city not found', 'is-danger')
        else:
            flash("This city already exist in database", "is-danger")
    return redirect(url_for('apiWeather'))


def get_weather_data(city): 
    """ Cette fonction permet de faire une requete vers l' api openWeather

        Arguments:
            city {[string]} -- le nom de la ville

        Returns:
            [json] -- dataset
    """
    yourapikey = '47c070163f772ba63244f399e7be83f2'
    units = 'metric'   #imperial cityname
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={yourapikey}&units={units}'
    r = requests.get(url)
    return r.json()
    

@app.route('/apiWeather/delete/<name>')
def apiWeather_delete_post(name):
    city = Weather.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()
    flash(f"{name} supprimée ", "is-success") # ou city.namr
    return redirect(url_for('apiWeather'))
    