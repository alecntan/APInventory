import os
import pytest

from apinventory import create_app
from apinventory.database import db


@pytest.fixture
def client():
    
    app = create_app('test_config.py')

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    #os.remove(app.config['DATABASE_PATH'])
    os.remove('/tmp/test.db')
    



