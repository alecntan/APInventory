import os
import pytest
from datetime import datetime 
from apinventory import create_app
from apinventory.database import *



@pytest.fixture
def client():
    
    app = create_app()

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

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

@pytest.fixture
def client_with_item():

    app = create_app('test_config.py')

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            new_storage = Storage(date=datetime.now(), name='box-A', location='stage right', notes='good!')
            db.session.add(new_storage)
            db.session.commit()

            cable_category = Category(name='Cable')
            db.session.add(cable_category)
            db.session.commit()

            new_item = Item(date=datetime.now()
                            ,name='hdmi'
                            ,identifier='CABHDM01'
                            ,status='In Storage'
                            ,category_id=cable_category.id
                            ,owner='tech'
                            ,notes='In good condition!'
                            ,serialNumber='AABB'
                            ,storage_id=new_storage.id)
                            
            db.session.add(new_item)
            db.session.commit()

            new_item = Item(date=datetime.now()
                            ,name='xlr'
                            ,identifier='CABXLR01'
                            ,status='In Usage'
                            ,category_id=cable_category.id
                            ,owner='tech'
                            ,notes='In good condition!'
                            ,serialNumber='BBCC'
                            ,storage_id=new_storage.id)
                            
            db.session.add(new_item)
            db.session.commit()
 
        yield client

    os.remove(app.config['DATABASE_PATH'])

@pytest.fixture
def client_with_storages_and_items():

    app = create_app('test_config.py')

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            new_storage_A = Storage(date=datetime.now(), name='box-A', location='stage right', notes='good!')
            new_storage_B = Storage(date=datetime.now(), name='box-B', location='stage left', notes='great!')
            db.session.add(new_storage_A)
            db.session.add(new_storage_B)
            db.session.commit()

            cable_category = Category(name='Cable')
            db.session.add(cable_category)
            db.session.commit()

            new_item = Item(date=datetime.now()
                            ,name='hdmi'
                            ,identifier='CABHDM01'
                            ,status='In Storage'
                            ,category_id=cable_category.id
                            ,owner='tech'
                            ,notes='In good condition!'
                            ,serialNumber='AABB'
                            ,storage_id=new_storage_A.id)
                            
            db.session.add(new_item)
            db.session.commit()

            new_item = Item(date=datetime.now()
                            ,name='xlr'
                            ,identifier='CABXLR01'
                            ,status='In Usage'
                            ,category_id=cable_category.id
                            ,owner='tech'
                            ,notes='In good condition!'
                            ,serialNumber='BBCC'
                            ,storage_id=new_storage_A.id)
                            
            db.session.add(new_item)
            db.session.commit()
 
        yield client

    os.remove(app.config['DATABASE_PATH'])
