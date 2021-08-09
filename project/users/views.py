from project import app, db
from project.models import User
from flask import Blueprint, flash, render_template, url_for, redirect, request, abort
from project.users.forms import RegisterForm, LoginForm, UpdateUserForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

user_blueprint = Blueprint('user', __name__, template_folder='templates/users')


@user_blueprint.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print("Inside Validate method")
        name = form.name.data
        username = form.username.data
        email = form.user_email.data
        password = form.user_password.data
        role = form.role.data
        # checking the existence of username, it goes to forms class and then calls the method. the method will return
        # none if the user is not present else will return a value
        if form.check_username(username) or form.check_email(email):
            flash("UserName or Email Already Registered")
            print("UserName or Email Already Registered")
            return render_template('register.html', form=form)
        user1 = User(name=name, role=role, username=username, user_email=email, user_password=password)
        print(user1)
        db.session.add(user1)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

# login method
@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    print("Inside login form")
    form = LoginForm()
    if form.validate_on_submit():
        print("inside vlaidate login")
        username = form.username.data
        password = form.user_password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.validate_password(password):
            login_user(user)
            print("Logged IN")
            role = user.role  # sending the role to welcome page
            return render_template('welcome.html', role=role)
        else:
            flash("Invalid username or password")
            return redirect(url_for('user.login'))
    return render_template('user_login.html', form=form)

# method to update username, email, password
@login_required
@user_blueprint.route('/update', methods=['GET', 'POST'])
def update():
    update_form = UpdateUserForm()
    user = User.query.get_or_404(current_user.id)
    if update_form.validate_on_submit():
        print("inside validate method")
        user.username = update_form.username.data
        user.user_email = update_form.email.data
        user.user_password = generate_password_hash(update_form.password.data)  # store the secured hash password in db
        db.session.commit()
        flash("Your account has been updated")
        return render_template('home.html')
    elif request.method =='GET':
        print("Inside GET Method")
        update_form.username.data = user.username
        update_form.email.data = user.user_email
        update_form.password.data = user.user_password
        return render_template('user_update.html', form=update_form)


# welcome page
@login_required
@user_blueprint.route('/welcome')
def welcome():
    if current_user.is_authenticated:
        role = current_user.role
        username = current_user.username
        print("Inside Welcome MEthod", role)
        return render_template('welcome.html', role=role, username=username)
    else:
        abort(403)

# logout user
@login_required
@user_blueprint.route('/logout')
def logout():
    logout_user()
    flash("You are logged out now")
    return render_template('home.html')