from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'  # this is to redirect user to login page when they try
                                        # to access any page which they are not authorized

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app, db)

@app.route('/')
def index():
    print("Inside Index Method")
    return render_template('home.html')


# import all the blueprints down here
from project.users.views import user_blueprint
from project.course.views import course_blueprint
from project.error_pages.views import error_blueprint
from project.student.view import student_blueprint


app.register_blueprint(error_blueprint)
app.register_blueprint(course_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(student_blueprint)
