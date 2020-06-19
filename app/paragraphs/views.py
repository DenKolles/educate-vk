import os


from flask import Blueprint, current_app, redirect, url_for, render_template, request, send_file
from werkzeug.utils import secure_filename

from app import db
from app.models import Course, Lecture, Paragraph
from app.paragraphs.forms import NewParagraphForm
from app.paragraphs.utils import save_file
from app.posts.forms import NewPostForm

paragraphs = Blueprint('paragraphs', __name__)


@paragraphs.route('/course/<int:course_id>/lecture/<int:lecture_id>/paragraph/new', methods=['GET', 'POST'])
def create_paragraph(course_id, lecture_id):
    form = NewParagraphForm()
    post_form = NewPostForm()
    course = Course.query.get_or_404(course_id)
    lecture = course.lectures[lecture_id-1]
    if form.validate_on_submit():
        if form.content.data:
            filename = secure_filename(form.content.data.filename)
            upload_path = os.path.join(current_app.root_path, 'static/course_materials', filename)
            form.content.data.save(upload_path)
            paragraph = Paragraph(name=form.name.data, content=upload_path, lecture_id=lecture.id)
            db.session.add(paragraph)
            db.session.commit()
        return redirect(url_for('lectures.get_lecture', course_id=course_id, lecture_id=lecture.id, post_form=post_form))
    return render_template('new_paragraph.html', title='New Paragraph', form=form, lecture_name=lecture.name)


@paragraphs.route('/download/<path:file_path>', methods=['GET', 'POST'])
def download_file(file_path):
    return send_file(file_path, as_attachment=True)


@paragraphs.route("/course/<int:course_id>/lecture/<int:lecture_id>/paragraph/<int:paragraph_id>/delete", methods=['POST'])
def delete_paragraph(course_id, lecture_id, paragraph_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('main.index'))
