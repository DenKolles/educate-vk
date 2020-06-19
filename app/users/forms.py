from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from app.models import User, Role, Group


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role_id = RadioField('Select Who You Are', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def __init__(self):
        super(RegistrationForm, self).__init__()
        self.role_id.choices = [(role.id, role.label) for role in Role.query.limit(2)]


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email')
    first_name = StringField('First name',
                             validators=[Length(min=2, max=20)])
    last_name = StringField('Last name',
                            validators=[Length(min=2, max=30)])
    group_id = SelectField('Please select your group (if you\'re from university)', coerce=int)
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def __init__(self):
        super(UpdateAccountForm, self).__init__()
        self.group_id.choices = [(group.id, group.name + ', ' + group.stakeholders) for group in Group.query.all()]
