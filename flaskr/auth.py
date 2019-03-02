import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

AUTH_PREEFIX = '/auth'
BLUEPRINT_NAME = 'auth'

bp = Blueprint(BLUEPRINT_NAME, __name__, url_prefix=AUTH_PREEFIX)