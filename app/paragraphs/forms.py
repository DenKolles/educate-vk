from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired


class NewParagraphForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=10, max=120)])
    content = image = FileField('Upload a file',
                                validators=[FileAllowed(['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'pdf', 'zip', 'rar'])])
    submit = SubmitField('Add paragraph')
