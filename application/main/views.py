from flask import render_template, Blueprint




from flask import Blueprint

main = Blueprint('main', __name__)



# filter personnalité tres utile
@main.template_filter('formatted_date')
def formatted_date(dt):
    return dt.strftime('%d %b %Y')


@main.route('/')
@main.route('/home')
def home():
    return render_template('pages/home.html', posts=posts)


@main.route('/contact')
def contact():
    return render_template('pages/contact.html', posts=posts)


@main.route('/about')
def about():
    return render_template('pages/about.html')
