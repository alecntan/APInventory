import os
from apinventory import create_app, db

app=create_app(testing=False)

# If it does not exist - create
with app.app_context():

    if not os.path.isfile(app.config['DATABASE_PATH']):
        db.create_all()
