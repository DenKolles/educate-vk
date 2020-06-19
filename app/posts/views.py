from flask import Blueprint, redirect, url_for
from flask_login import current_user

from app import db
from app.models import Course, Post
from app.posts.forms import NewPostForm

posts = Blueprint('posts', __name__)


@posts.route('/course/<int:course_id>/lecture/<int:lecture_id>/paragraph/<int:paragraph_id>/post/new', methods=['GET', 'POST'])
def create_post(course_id, lecture_id, paragraph_id):
    form = NewPostForm()
    course = Course.query.get_or_404(course_id)
    lecture = course.lectures[lecture_id-1]
    paragraph = lecture.paragraphs[paragraph_id]
    if form.validate_on_submit():
        post = Post(content=form.content.data, paragraph_id=paragraph.id, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
    return redirect(url_for('lectures.get_lecture', course_id=course_id, lecture_id=lecture.id, post_form=form))
