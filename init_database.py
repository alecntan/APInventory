from  app.database import *
from app import create_app

from datetime import datetime
import random
import os

# Storage Data
date = datetime.now()
storage_names = ['box-A', 'box-B', 'box-C', 'box-D']
storage_locations = ['floor A', 'floor B', 'floor C']
notes = ['good!', 'bad!', 'meh']

# Item Data
name = ['xlr', 'hdmi', 'lead', 'iMac', 'desktop', 'monitor']
identifier = ['a', 'b', 'c', 'd', 'e']
status = ['In storage', 'In use', 'broken', 'missing']
category = ['cable', 'device', 'adaptor']
owner = ['tech', 'creative', 'music']
serialNumber = ['aaa', 'bbb', 'ccc', 'eee']

app = create_app()

with app.app_context():

    if os.path.isfile('/tmp/test.db'):
        os.remove('/tmp/test.db')

    db.create_all()

    for s in range(len(storage_names)):

        loc_index = random.randrange(0, len(storage_locations))
        notes_index = random.randrange(0, len(notes))

        name = storage_names[s]
        loc = storage_locations[loc_index]
        note = notes[notes_index]

        new_storage = Storage(date=date, name=name, location=loc, notes=note)
        db.session.add(new_storage) 
        db.session.commit()


    # Add items
    xlr1 = Item(date=date, name='xlr', identifier='CABXLR01', status='In use', category='cable', owner='tech', serialNumber='AAABBB', storage_id=1)
    xlr2 = Item(date=date, name='xlr', identifier='CABXLR02', status='In use', category='cable', owner='tech', serialNumber='AAABBB', storage_id=1)
    xlr3 = Item(date=date, name='xlr', identifier='CABXLR03', status='In use', category='cable', owner='tech', serialNumber='AAABBB', storage_id=1)
    xlr4 = Item(date=date, name='xlr', identifier='CABXLR04', status='In use', category='cable', owner='tech', serialNumber='AAABBB', storage_id=1)

    
    hdmi1 = Item(date=date, name='hdmi', identifier='CABHDM01', status='In use', category='cable', owner='tech', serialNumber='AAABBB', storage_id=2)
    hdmi2 = Item(date=date, name='hdmi', identifier='CABHDM02', status='In use', category='cable', owner='tech', serialNumber='AAABBB', storage_id=2)
    hdmi3 = Item(date=date, name='hdmi', identifier='CABHDM03', status='In use', category='cable', owner='tech', serialNumber='AAABBB', storage_id=3)

    hdmi4 = Item(date=date, name='hdmi', identifier='CABHDM04', status='In use', category='cable', owner='tech', serialNumber='AAABBB', storage_id=4)
    hdmi5 = Item(date=date, name='hdmi', identifier='CABHDM05', status='In use', category='cable', owner='tech', serialNumber='AAABBB', storage_id=4)

    db.session.add(xlr1)
    db.session.add(xlr2)
    db.session.add(xlr3)
    db.session.add(xlr4)

    db.session.add(hdmi1)
    db.session.add(hdmi2)
    db.session.add(hdmi3)
    db.session.add(hdmi4)
    db.session.add(hdmi5)


    db.session.commit()





    


    










