
from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)



@errors.app_errorhandler(403)
def page_not_found(e):
    # note that we set the 403 status explicitly
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def page_not_found(e):
    # note that we set the 500 status explicitly
    return render_template('errors/500.html'), 500
