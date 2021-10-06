import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from ledger import default_config
from ledger.database import *


def create_app(config_file=None):
    
    app = Flask(__name__)
    app.config.from_object(default_config)

    if config_file != None:
        app.config.from_pyfile(config_file, silent=True)
  
    # Initialise Packages
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def hello():
        return 'Hello World!\n'

    
    # Set Blueprints here

    return app
   

