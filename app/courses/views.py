from flask import Blueprint, render_template, redirect, url_for
from flask_user import roles_required

from app import db
from app.models import Course

courses = Blueprint('courses', __name__)


@courses.route('/course/new', methods=['GET', 'POST'])
def create_course():
    # form = PredictionForm()
    # if form.validate_on_submit():
    #     for image in form.image.data:
    #         if image:
    #             save_prediction_image(image)
    #             image_path = os.path.join(current_app.root_path, 'static/prediction_images', image.filename)
    #             prediction = predict_image(image_path)
    #             full_prediction = Prediction(image_file=image.filename,
    #                                          user_id=current_user.id,
    #                                          class_id=prediction['class_id'],
    #                                          probability=prediction['probability'])
    #             db.session.add(full_prediction)
    #     db.session.commit()
    #     return redirect(url_for('main.index'))
    # return render_template('predict.html', title='Predict', form=form)
    return


@courses.route("/course/<int:course_id>")
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course.html', course=course, edit_enable=False)


@courses.route("/course/<int:course_id>/edit")
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course.html', course=course, edit_enable=True)


@courses.route("/course/<int:course_id>/delete", methods=['POST'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('main.index'))


@courses.route("/course/<int:course_id>/rate/<int:rating>")
def rate_course(course_id, rating):
    course = Course.query.get_or_404(course_id)
    course.votes += 1
    course.rating = course.rating + rating
    db.session.commit()
    return redirect(url_for('courses.get_course', course_id=course.id, edit_enable=False))
