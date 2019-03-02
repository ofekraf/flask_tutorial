import os
from flask import Flask

#file locations
SECRET_KEY_VAL = 'dev' # todo  - should be overridden with a random value when deploying.
CONFIG_FILE_PATH = 'config.py'
DATABASE_FILE_PATH = 'flaskr.sqlite'
HELLO_APP_RETURNED_MESSAGE = 'My flask site is better than your flask site!'


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY_VAL,
        DATABASE=os.path.join(app.instance_path, DATABASE_FILE_PATH),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile(CONFIG_FILE_PATH, silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return HELLO_APP_RETURNED_MESSAGE

    from . import db
    db.init_app(app)

    return app