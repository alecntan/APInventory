import os
from flask import Flask
from app.config import Default


def create_app(config_filename='my_config.py'):

    app = Flask(__name__, instance_relative_config=True)

    # Load Default
    app.config.from_object(Default)

    # Override default config (if exists)
    if config_filename is not None:
        app.config.from_pyfile(config_filename, silent=True)

    # ensures the instance folder exists
    try:
        os.makedirs(app.instance_path) # Default instance path is used

    except OSError:
        pass


    @app.route('/')
    def index():
        return app.config['MSG']
    

    return app

