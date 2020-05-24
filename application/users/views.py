
# from flask_sqlalchemy import sqlalchemy # pour utliser la fonction desc de sqlalchemy . Remarque # from flask_sqlalchemy.sqlalchemy import desc , ne marche pas , why??
from flask import render_template, url_for, flash, redirect, request
from application import app, db, bcrypt, mail
from application.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                RequestResetForm, ResetPasswordForm)
from application.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message



from flask import Blueprint

users= Blueprint('users',__name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    # and form.validate()  # envoyer un message flash de succes et retour a la page d'accueil
    if request.method == 'POST' and form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(
            form.password.data).decode('utf8')
        user = User(username=form.username.data,
                    email=form.email.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash(f' Welcome you are registered in!', 'is-success')
        return redirect(url_for('login'))
    return render_template('pages/register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Good! You have been logged in.', 'is-succes')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessul. Try again! Your credentials is false', 'is-danger')
    return render_template('pages/login.html', title='login', form=form)



@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@users.route('/account', methods=['GET', 'POST'])
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
    image_file = url_for(
        'static', filename='src/img/profile_pics/' + current_user.image_file)
    return render_template('pages/account.html', title='account', image_file=image_file, form=form)


@useers.route('/user_post/<string:username>')
def user_post(username):
    page = request.args.get('page', 1, type=int)

    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,  per_page=3)
    return render_template('pages/blogs/user_post.html',  posts=posts, user=user, title='All User Posts')


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        send_reset_email(user)
        flash(' Un mail vous a ete envoyé avec les instructions pour initialiser votre password', 'is-success')
        return redirect(url_for('login'))
    return render_template('pages/reset_request.html', form=form, title='Request Reset Password')


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'is-danger')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    # and form.validate()  # envoyer un message flash de succes et retour a la page d'accueil
    if request.method == 'POST' and form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(
            form.password.data).decode('utf8')
        user.password = password_hash
        db.session.commit()
        flash(f' Votre password a ete mise à jour, vous pouvez maintenant vous connectez!', 'is-success')
        return redirect(url_for('login'))

    return render_template('pages/reset_token.html', form=form, title='Reset Password')





@users.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AdminForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'admin':
            print('youre login !!!')
            redirect(url_for('home'))
    return render_template('admin/index.html', form=form)
