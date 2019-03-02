import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db


#SQL COMMANDS
INSERT_NEW_USER_SQL_COMMAND = 'INSERT INTO user (username, password) VALUES (?, ?)'
CHECK_EXISTING_USERNAME_SQL_QUERY = 'SELECT id FROM user WHERE username = ?'

#error messages
MISSING_PASSWORD_ERROR = 'Password is required.'
EXISTING_USERNAME_ERROR = 'User {} is already registered.'
MISSING_USERNAME_ERROR = 'Username is required.'

AUTH_PREEFIX = '/auth'
BLUEPRINT_NAME = 'auth'

bp = Blueprint(BLUEPRINT_NAME, __name__, url_prefix=AUTH_PREEFIX)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = check_error_user_registration(db, password, username)
        if error is None:
            db.execute(INSERT_NEW_USER_SQL_COMMAND,(username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login')) #todo - change to constant?
        flash(error)
    return render_template('auth/register.html') #todo - change to constant?


def check_error_user_registration(db, password, username):
    """ :return: an error is such occurred. None otherwise    """
    error = None
    if not username:
        error = MISSING_USERNAME_ERROR
    elif not password:
        error = MISSING_PASSWORD_ERROR
    elif db.execute(CHECK_EXISTING_USERNAME_SQL_QUERY,
                    (username,)).fetchone() is not None:
        error = EXISTING_USERNAME_ERROR.format(username)
    return error


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')