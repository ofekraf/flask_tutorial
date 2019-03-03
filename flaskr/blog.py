from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

BLOG_POST_SQL_QUERY = 'SELECT p.id, title, body, created, author_id, username' \
    ' FROM post p JOIN user u ON p.author_id = u.id' \
    ' ORDER BY created DESC'

bp = Blueprint('blog',__name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(BLOG_POST_SQL_QUERY).fetchall()
    return render_template('blog/index.html', posts=posts)