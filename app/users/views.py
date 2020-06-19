from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app.users.utils import save_avatar
from app import db, bcrypt
from app.users.forms import LoginForm, RegistrationForm, UpdateAccountForm
from app.models import User, Course

from flask import Blueprint

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, role_id=form.role_id.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Successfully registered. You can now log in', 'success')
        return redirect(url_for('main.index'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/account", methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_avatar(form.picture.data)
            current_user.avatar = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.group_id = form.group_id.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.group_id.data = current_user.group_id
    image_file = url_for('static', filename='profile_pics/' + current_user.avatar)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/sub/<int:course_id>", methods=['GET', 'POST'])
def subscribe(course_id):
    if current_user.is_authenticated:
        course = Course.query.get(course_id)
        current_user.courses.append(course)
        db.session.commit()
        return redirect(url_for('courses.get_course', course_id=course_id, edit_enable=False))
    else:
        flash('You need to have an account for that. Consider registering.', 'danger')
    return redirect(url_for('users.register'))


@users.route("/unsub/<int:course_id>", methods=['GET', 'POST'])
def unsubscribe(course_id):
    course = Course.query.get(course_id)
    current_user.courses.remove(course)
    db.session.commit()
    return redirect(url_for('main.index'))
