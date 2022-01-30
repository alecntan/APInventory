import os
from flask import Flask
from .config import Default

from .database import db

def create_app(config_filename=None):

    app = Flask(__name__, instance_relative_config=True)
    
    # Load Default
    app.config.from_object(Default)

    # Load Extensions
    db.init_app(app)

    # Override default config (if exists)
    if config_filename != None:
        app.config.from_pyfile(config_filename, silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import inventory
    app.register_blueprint(inventory.inventory)

    return app

