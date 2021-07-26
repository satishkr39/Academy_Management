from datetime import datetime

from project import login_manager, app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from wtforms.validators import ValidationError

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    role = db.Column(db.String(20))
    username = db.Column(db.String(20), unique=True)
    user_email = db.Column(db.String(60), unique=True)
    user_password = db.Column(db.String(40), index=True)
    # a teacher can have multiple course
    course = db.relationship('Course', backref='user_ref', lazy='dynamic')

    def __init__(self, name, role, username, user_email, user_password):
        self.name = name
        self.role = role
        self.username = username
        self.user_email = user_email
        self.user_password = generate_password_hash(password=user_password)

    def __repr__(self):
        return f"The username is {self.username} and email is {self.user_email}"

    def validate_password(self, password):
        return check_password_hash(self.user_password, password=password)

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))
    # linking a course to user table ID column
    course_instructor = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    course_fee = db.Column(db.Integer)
    course_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    course_duration = db.Column(db.Integer, nullable=False)

    def __init__(self, course_name, course_instructor, course_fee, course_created, course_duration):
        self.course_name = course_name
        self.course_instructor = course_instructor
        self.course_fee = course_fee
        self.course_duration = course_duration
        self.course_created= course_created

    def __repr__(self):
        return f"The course name is {self.course_name}, instructor name is {self.course_instructor}, " \
               f"fee is {self.course_fee}, created on {self.course_created}, duration is {self.course_duration}"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    s_course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    date_enrolled = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)

    def __init__(self, user_id, s_course_id, date_enrolled):
        self.user_id = user_id
        self.s_course_id = s_course_id
        self.date_enrolled = date_enrolled

    def __repr__(self):
        return f"The user is is {self.user_id}, course_id is {self.s_course_id} and date enrolled is {self.date_enrolled}"