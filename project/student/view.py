from project import db, app, login_manager
from flask import Blueprint, render_template, url_for, flash, abort, redirect, request
from flask_login import login_manager, login_required, current_user
from project.models import User, Course, Student
from datetime import datetime
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
@student_blueprint.route('/enroll_course')
@login_required
def enroll_course():
    print("Inside Enroll Course")
    course_id = request.args.get('course_id')
    course_details = Course.query.get_or_404(course_id)  # tries to get course for course_id, if not found then 404 error page
    # need to check whether the use has already enrolled for the course or not. if already enrolled then throw error
    course_check = Student.query.filter_by(user_id=current_user.id, s_course_id=course_id).all()
    if len(course_check) > 0:  # if registered then throw error message
        print("User already enrolled")
        flash("You are already enrolled in the course. Thank You.")
        return redirect(url_for('student.student_view_course'))
    student = Student(user_id=current_user.id, s_course_id=course_id, date_enrolled=datetime.utcnow())
    db.session.add(student)
    db.session.commit()
    flash("Thank you for enrolling in the course!!!")
    return redirect(url_for('student.student_view_course'))


# view course for which they are enrolled
@student_blueprint.route('/view_enrolled_course')
@login_required
def view_enrolled_course():
    print("Inside View Enrolled Course")


