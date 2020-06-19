from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class NewPostForm(FlaskForm):
    content = StringField('Write your comment',
                       validators=[DataRequired(), Length(min=10, max=120)])
    submit = SubmitField('Send')
