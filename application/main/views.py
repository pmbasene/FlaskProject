from flask import render_template, Blueprint




from flask import Blueprint

main = Blueprint('main', __name__)



# filter personnalité tres utile
@main.app_template_filter('formatted_date')
def formatted_date(dt):
    return dt.strftime('%d %b %Y')


@main.route('/')
@main.route('/home')
def home():
    return render_template('pages/home.html')


@main.route('/contact')
def contact():
    return render_template('pages/contact.html')


@main.route('/about')
def about():
    return render_template('pages/about.html')


@main.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AdminForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'admin':
            print('youre login !!!')
            redirect(url_for('home'))
    return render_template('admin/index.html', form=form)




# my stuff
@main.route('/testjs')
def testjs():
    return render_template('testjs.html')

# -----route for testing-----


@main.route('/garage')     # for integrating video format
def garage():
    return render_template('pages/garage.html', title='Garage tools')

