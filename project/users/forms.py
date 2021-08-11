from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, PasswordField
from wtforms.validators import Email, DataRequired
from project.models import User

class RegisterForm(FlaskForm):
    name = StringField("Enter your name : ", validators=[DataRequired()])
    role = RadioField("Select your role: ", choices=[('student','Enroll as student'),
                                                                 ('Teacher','Enroll as Teacher')],
                                          validators=[DataRequired()])
    username = StringField("Enter unique username", validators=[DataRequired()])
    user_email = StringField("Enter your email ID: ", validators=[Email()])
    user_password = PasswordField("Enter your password", validators=[DataRequired()])
    submit = SubmitField("Click to register")

    # method to check for duplicate username,the method is called in views.py of user section
    def check_username(self, username):
        return User.query.filter_by(username=username).first()

    def check_email(self, email):
        return User.query.filter_by(user_email=email).first()



class LoginForm(FlaskForm):
    username = StringField("Enter unique username", validators=[DataRequired()])
    user_password = PasswordField("Enter your password", validators=[DataRequired()])
    submit = SubmitField("Login")


class UpdateUserForm(FlaskForm):
    username = StringField("Enter unique username", validators=[DataRequired()])
    email = StringField("Enter your email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Enter new password: ", validators=[DataRequired()])
    submit = SubmitField("Click to update")