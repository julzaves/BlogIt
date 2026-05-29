from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from dotenv import load_dotenv
import dotenv
import os

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_test_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    dotenv.load_dotenv()

    # ensure the instance folder exists before building the DB path
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    test_db_path = os.path.join(app.instance_path, 'test.db')
    app.config.from_mapping(
        TESTING=True,
        # a default secret that should be overridden by instance config
        SECRET_KEY=os.urandom(16),
        # store the database in the instance folder
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{test_db_path}?check_same_thread=False',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    app.app_context().push()  # this does the binding

    @app.route("/hello")
    def hello():
        return os.getenv('DATABASE_URL')

    # initialize plugins
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'
    bcrypt.init_app(app)

    # apply the blueprints to the app
    from blogit import routes

    # register blueprint
    app.register_blueprint(routes.bp)

    # make url_for('index') == url_for('blog.index')
    app.add_url_rule("/", endpoint="index")

    return app

def create_development_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    load_dotenv()

    # ensure the instance folder exists before building the DB path
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    site_db_path = os.path.join(app.instance_path, 'site.db')
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY=os.urandom(16),
        # store the database in the instance folder
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', f'sqlite:///{site_db_path}'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    app.app_context().push()  # this does the binding

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # initialize plugins
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'
    bcrypt.init_app(app)
    migrate = Migrate(app, db)

    # apply the blueprints to the app
    from blogit import routes

    # register blueprint
    app.register_blueprint(routes.bp)

    # make url_for('index') == url_for('blog.index')
    app.add_url_rule("/", endpoint="index")

    return app



