from flask import Blueprint, render_template, url_for, redirect
from flask_user import roles_required, login_required

from app import db
from app.lectures.forms import NewLectureForm
from app.models import Lecture, Course
from app.posts.forms import NewPostForm

lectures = Blueprint('lectures', __name__)


@lectures.route('/course/<int:course_id>/lecture/new', methods=['GET', 'POST'])
def create_lecture(course_id):
    form = NewLectureForm()
    course = Course.query.get_or_404(course_id)
    if form.validate_on_submit():
        lecture = Lecture(name=form.name.data, description=form.description.data, course_id=course_id)
        db.session.add(lecture)
        db.session.commit()
        return redirect(url_for('courses.get_course', course_id=course_id, edit_enable=True))
    return render_template('new_lecture.html', title='New Lecture', form=form, course_name=course.name)


@lectures.route("/course/<int:course_id>/lecture/<int:lecture_id>", methods=['GET', 'POST'])
def get_lecture(course_id, lecture_id):
    post_form = NewPostForm()
    course = Course.query.get_or_404(course_id)
    lecture = course.lectures[lecture_id-1]
    return render_template('lecture.html', lecture=lecture, post_form=post_form)


@lectures.route("/course/<int:course_id>/lecture/<int:lecture_id>/delete", methods=['POST'])
def delete_lecture(course_id, lecture_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('main.index'))


@lectures.route("/course/<int:course_id>/lecture/<int:lecture_id>/rate/<int:rating>")
def rate_lecture(course_id, lecture_id, rating):
    course = Course.query.get_or_404(course_id)
    course.votes += 1
    course.rating = course.rating + rating
    db.session.commit()
    return redirect(url_for('courses.get_course', course_id=course.id, edit_enable=False))
