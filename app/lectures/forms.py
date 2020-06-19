from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired


class NewLectureForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=10, max=120)])
    description = TextAreaField('Description (optional)',
                              validators=[Length(max=500)])
    submit = SubmitField('Create')
