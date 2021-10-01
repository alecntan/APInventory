import os
from flask import Flask

def create_app(config_file=None):
    
    # instance_relative_conifg => loads config files (e.g. from_pyfile) relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('ledger.default_config')

    if config_file != None:
        app.config.from_pyfile(config_file, silent=True)

    
    # ensure that the instance folder exists
    try:
        os.makedirs(app.instance_path)

    except OSError:
        pass


    @app.route('/', methods=['GET'])
    def hello():
        return 'Hello World!\n'

    
    # Set Blueprints here

    return app
    
