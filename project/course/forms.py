from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_login import UserMixin

class AddCourseForm(FlaskForm, UserMixin):
    course_name = StringField("Enter the course Name: ", validators=[DataRequired()])
    course_fee = IntegerField("Enter the total course fees: ", validators=[DataRequired()])
    course_duration = IntegerField("Enter the course duration in hours: ", validators=[DataRequired()])
    course_creation = DateField("Enter the date created for course: ",format='%m/%d/%Y', validators=[DataRequired()])
    submit = SubmitField("Create Course")

class DeleteCourseForm(FlaskForm, UserMixin):
    course_id = IntegerField("Enter the course id to be deleted")
    submit = SubmitField("Delete the course")


class UpdateCourseForm(FlaskForm, UserMixin):
    course_name = StringField("Enter the new course name")
    course_fee = IntegerField("Enter the new revised course fees")
    course_duration = IntegerField("Enter the new revised duration: ")
    submit = SubmitField("Update Course")