from project import db, app, login_manager
from flask import Blueprint, render_template, url_for, flash, abort, redirect, request
from flask_login import login_manager, login_required
from project.models import User, Course

student_blueprint = Blueprint('student', __name__, template_folder='templates/student')


# view all courses irrespective of trainers
@student_blueprint.route('/student_view_course')
@login_required
def student_view_course():
    print("Inside Student View Course")
    page = request.args.get('page', 1, type=int)
    print("Page number is :", page)
    all_course = Course.query.order_by(Course.course_created.desc()).paginate(page=page, per_page=3)
    return render_template('student_view_course.html', course=all_course)

# enroll in a course
@student_blueprint.route('/enroll_course/<course_id>')
@login_required
def enroll_course(course_id):
    pass
