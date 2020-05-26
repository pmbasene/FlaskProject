from application import app,  mail
from flask_mail import Message
import os
from PIL import Image
import secrets
from flask import url_for


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


def send_reset_email(user):
    # _external = True enable to have absolute path url ranter than relative path
    token = user.get_reset_token()
    msg = Message('password Reset Resquest',
                  sender='basene89@gmail.com',
                  recipients=[user.email])

    msg.body = f''' To reset your password , visit to following link:
        {url_for('reset_token', token=token, _external= True)}.
        if you did not make this request then simply ignore this email.
        
        '''
    mail.send(msg)
