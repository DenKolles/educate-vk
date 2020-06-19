from datetime import datetime

from flask_login import UserMixin

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


course_user = db.Table('course_user', db.metadata,
                       db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                       )

db.Index('c_u_ind', course_user.c.course_id, course_user.c.user_id, unique=True)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=True)
    avatar = db.Column(db.String(20), nullable=False, default='default.jpg')
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(60), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    group = db.relationship('Group', foreign_keys=[group_id], backref='students', lazy='select')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role')
    courses = db.relationship('Course', secondary="course_user", back_populates='pupils', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.avatar}')"

    def fullname(self):
        if self.last_name is None or self.first_name is None:
            return ""
        return f"{self.last_name} {self.first_name}"

    def initials(self):
        if self.last_name is None or self.first_name is None:
            return ""
        return f"{self.last_name} {self.first_name[0]}."

    def is_lector(self):
        if self.role.name == "lector":
            return True
        return False



class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)
    label = db.Column(db.Unicode(255), server_default=u'')


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    rules = db.Column(db.String(126), nullable=True)
    stakeholders = db.Column(db.String(60), unique=True, nullable=True)
    certificate = db.Column(db.String(12), nullable=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.stakeholders}', '{self.manager.__repr__()}')"


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    picture = db.Column(db.String(12), nullable=True, default='default.jpg')
    rating = db.Column(db.Float, default=0)
    votes = db.Column(db.Integer, default=0)
    lectures = db.relationship('Lecture', backref='course', lazy='select')
    pupils = db.relationship('User', secondary="course_user", back_populates='courses', lazy='dynamic')
    lector_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lector = db.relationship('User', foreign_keys=[lector_id])

    def __repr__(self):
        return f"Course('{self.id}', '{self.name}, rated {self.rating} from {self.votes} votes')"


class Lecture(db.Model):
    __tablename__ = 'lecture'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Float, default=0)
    votes = db.Column(db.Integer, default=0)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    paragraphs = db.relationship('Paragraph', backref='lecture', lazy='select')

    def __repr__(self):
        return f"Lecture('{self.id}', '{self.name}')"


class Paragraph(db.Model):
    __tablename__ = 'paragraph'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(12), nullable=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)
    posts = db.relationship('Post')

    def __repr__(self):
        return f"Paragraph('{self.id}', '{self.name}')"


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float, default=0)
    votes = db.Column(db.Integer, default=0)
    paragraph_id = db.Column(db.Integer, db.ForeignKey('paragraph.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User')

    def __repr__(self):
        return f"Paragraph('{self.author.__repr__()}', '{self.content}')"
