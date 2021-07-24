from project.course.forms import AddCourseForm, DeleteCourseForm, UpdateCourseForm
from project import db, app
from flask import render_template, url_for, redirect, Blueprint, abort, session, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from project.models import Course, User

course_blueprint = Blueprint('course', __name__, template_folder='templates/course')

# Add New course by trainer
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
            # if the user enter invalid course id then dispaly error message and render the same page again
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


# update course : A trainer can update course_name, course_fee, course_duration
@course_blueprint.route('/update/<course_id>', methods=['GET', 'POST'])
@login_required
def update_course(course_id):
    print("Inside Upate Course Method and course id is ", course_id)
    # this to get the updates from html form
    update_form = UpdateCourseForm()
    course_details = Course.query.filter_by(course_id=course_id).first()  # get course details by using its ID
    if update_form.validate_on_submit():
        print("Inside IF Statement")
        course_details.course_name = update_form.course_name.data
        course_details.course_fee = update_form.course_fee.data
        course_details.course_duration = update_form.course_duration.data
        print("COurse New Details are :")
        db.session.commit()  # update doesn't require to add before committing
        return "Update in Else"
    elif request.method == 'GET':
        print("Inside ELSE Statement")
        # this is to fill the form when the user opens it for updating
        update_form.course_name.data = course_details.course_name  # pre-fill the course_name
        update_form.course_fee.data = course_details.course_fee  # pre-fill the course fee
        update_form.course_duration.data = course_details.course_duration  # pre-fill the course duration
        return  render_template('update_course.html', form=update_form)



# view all course and will be filtered by trainer
@course_blueprint.route('/view_course')
@login_required
def view_course():
    session['condition'] = False
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        all_course = Course.query.filter_by(course_instructor=current_user.username).order_by(Course.course_created.desc()).paginate(page=page, per_page=3)
        '''for page_num in all_course.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2):
            print("Iter Pages: ", page_num)
        print("All course Page: ", all_course.page)'''  # since all course is pagination object, so page attribute got appended to it
        return render_template('view_course.html', course=all_course)
    else:
        return redirect(url_for('error.error_403'))