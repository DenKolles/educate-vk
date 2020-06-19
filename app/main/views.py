from flask import render_template, request
from flask_login import current_user

from app.models import Course

from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    courses = Course.query.paginate(page=page, per_page=3)
    return render_template('index.html', courses=courses)
