from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


def create_app(config_name):

    app = Flask(__name__)

    #creating the app configurations
    app.config.from_object(config_options[config_name])
    config_options[config_name]

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
