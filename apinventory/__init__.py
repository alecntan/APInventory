import os
from flask import Flask
from .config import Default

from .database import db

def create_app(testing=True):

    app = Flask(__name__, instance_relative_config=True)
    
    # Load Default
    app.config.from_object(Default)

    # Load Extensions
    db.init_app(app)


    # Override default config (if exists)
    if not testing:
        #app.config.from_pyfile(config_filename, silent=True)

        SECRET_KEY = os.environ.get('SECRET_KEY')
        SQLALCHEMY_DATABASE_URI  = os.environ.get('SQLALCHEMY_DATABASE_URI')
       
        if not SECRET_KEY:
            raise ValueError('No SECRET_KEY set for Flask application')
        
        app['SECRET_KEY'] = SECRET_KEY

        if not SQLALCHEMY_DATABASE_URI:
            raise ValueError('No SQLALCHEMY_DATABASE_URI set for flask application')

        app['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

        app['DEBUG'] = False
        app['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # ensures the instance folder exists
    try:
        os.makedirs(app.instance_path) # Default instance path is used

    except OSError:
        pass

    from . import inventory
    app.register_blueprint(inventory.inventory)
    
    return app

