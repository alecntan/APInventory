import os
import pytest
from datetime import datetime

from apinventory import create_app
from apinventory.database import db, Storage



@pytest.fixture
def client():
    
    app = create_app('test_config.py')

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    #os.remove(app.config['DATABASE_PATH'])
    os.remove(app.config['DATABASE_PATH'])
    

@pytest.fixture
def client_with_storage():

    app = create_app('test_config.py')

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            new_storage = Storage(date=datetime.now(), name='box-A', location='stage right', notes='good!')
            db.session.add(new_storage)
            db.session.commit()

        yield client

    os.remove(app.config['DATABASE_PATH'])
