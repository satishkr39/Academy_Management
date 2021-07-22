from project.course.forms import AddCourseForm, DeleteCourseForm
from project import db, app
from flask import render_template, url_for, redirect, Blueprint, abort, session, flash
from flask_login import login_required, login_user, logout_user, current_user
from project.models import Course, User

course_blueprint = Blueprint('course', __name__, template_folder='templates/course')


@course_blueprint.route('/add_course', methods=['POST', 'GET'])
@login_required
def add_course():
    print("Inside Add COurse Form")
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
            return redirect(url_for('course.view_course'))
        return render_template('add_course.html', form=form)
    else:
        abort(403)

# delete course
@course_blueprint.route('/delete', methods=['POST', 'GET'])
@login_required
def delete_course():
    print("Inside Delete Course")
    session['condition'] = True
    form = DeleteCourseForm()
    if current_user.is_authenticated:
        all_course = Course.query.filter_by(course_instructor=current_user.username).all()
        if form.is_submitted() and form.validate():
            print("Inside valid delete call")
            course_id = form.course_id.data
            print("THe ID got to be delted is : ", course_id)
            course_to_delete = Course.query.filter_by(course_id=course_id).first()
            if course_to_delete is None:
                flash("No course found to be deleted")
                return render_template('view_course.html', form=form, course=all_course, condition=session['condition'])
            print(course_to_delete)
            db.session.delete(course_to_delete)
            db.session.commit()
            deleted_mess = "Course ID deleted is: "+ str(course_id)
            flash(deleted_mess)
            return redirect(url_for('course.view_course'))
        return render_template('view_course.html',form=form, course=all_course,condition=session['condition'])
    else:
        abort(403)


# update course
# @course_blueprint.route('/update/<course_id:int>')

# view all course and will be filtered by trainer
@course_blueprint.route('/view_course')
@login_required
def view_course():
    session['condition'] = False
    if current_user.is_authenticated:
        print("Inside view course auth")
        all_course = Course.query.filter_by(course_instructor=current_user.username).all()
        print(all_course)
        return render_template('view_course.html', course=all_course)
    else:
        return redirect(url_for('error.error_403'))