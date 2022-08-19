import os

from dynaconf import FlaskDynaconf
from flask import Flask

from . import db
from .routes import secured_app, user


def create_app():
    app = Flask(__name__)
    FlaskDynaconf(app, settings_files=[".secrets.toml"])
    app.config.from_mapping(
        SECRET_KEY=app.config.SECRET_KEY,
        DATABASE=os.path.join(app.instance_path, "auth.sqlite"),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    # Routes
    app.register_blueprint(user.bp)
    app.register_blueprint(secured_app.bp)

    return app
