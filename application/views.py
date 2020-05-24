import requests
import os
import secrets
from PIL import Image
# from flask_sqlalchemy import sqlalchemy # pour utliser la fonction desc de sqlalchemy . Remarque # from flask_sqlalchemy.sqlalchemy import desc , ne marche pas , why??
from flask import render_template, url_for, flash, redirect, request, abort
from application import app, db , bcrypt, mail
from application.forms import (RegistrationForm , LoginForm, UpdateAccountForm, 
                               PostFrom, RequestResetForm, ResetPasswordForm)
from application.models import User, Post, Editor, Weather
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message





# my stuff
@app.route('/testjs')
def testjs():
    return render_template('testjs.html')

# -----route for testing----- 

@app.route('/garage')     # for integrating video format
def garage():
    return render_template('pages/garage.html', title='Garage tools')


