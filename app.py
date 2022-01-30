import os
from apinventory import create_app, db

app=create_app(config_filename='prod_config.py')

# If db does not exist - create
with app.app_context():

    if not os.path.isfile(app.config['DATABASE_PATH']):
        db.create_all()
