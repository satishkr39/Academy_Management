from project import app
from flask import Flask, Blueprint, url_for, render_template

error_blueprint = Blueprint('error', __name__, template_folder='templates/error_pages')

@error_blueprint.app_errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404

@error_blueprint.app_errorhandler(403)
def error_403(e):
    return render_template('403.html'), 403