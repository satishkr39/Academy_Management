from project.course.forms import AddCourseForm
from project import db, app
from flask import render_template, url_for, redirect, Blueprint, abort
from flask_login import login_required, login_user, logout_user, current_user
from project.models import Course

course_blueprint = Blueprint('course', __name__, template_folder='templates/course')

@login_required
@course_blueprint.route('/add_course', methods=['POST', 'GET'])
def add_course():
    print("Inside Add COurse Form")
    print(current_user.username)
    if current_user.is_authenticated:
        form = AddCourseForm()
        if form.is_submitted() and form.validate():
            print("Inside Validate Form Add Course")
            course_name = form.course_name.data
            course_fee = form.course_fee.data
            course_duration = form.course_duration.data
            course_creation = form.course_creation.data
            print(course_creation)
            course_instructor = current_user.username  # using UserMixin to get the current user details
            course_add = Course(course_name=course_name, course_instructor=course_instructor,
                                        course_fee=course_fee, course_created=course_creation, course_duration=course_duration)
            print(course_add)
            db.session.add(course_add)
            db.session.commit()
        return render_template('add_course.html', form=form)
    else:
        return "Please login"
