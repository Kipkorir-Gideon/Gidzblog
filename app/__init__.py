from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


def create_app(config_name):

    app = Flask(__name__)