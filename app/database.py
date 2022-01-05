from flask_sqlalchemy import SQLAlchemy

# CONSTRAINTS
MAX_NAME_LENGTH  = 25
MAX_LOC_LENGTH   = 50
MAX_NOTES_LENGTH = 120
MAX_STAT_LENGTH = 25
MAX_IDEN_LENGTH = 8
MAX_SERN_LENGTH = 50



db = SQLAlchemy()


class Storage(db.Model):
   
    id       = db.Column(db.Integer, primary_key=True) 
    date     = db.Column(db.Date, nullable=False)
    name     = db.Column(db.String(MAX_NAME_LENGTH), unique=True, nullable=False)
    location = db.Column(db.String(MAX_NAME_LENGTH), unique=True, nullable=False)
    notes    =  db.Column(db.String(MAX_NOTES_LENGTH), nullable=True)

    items    = db.relationship('Item', backref='storage', lazy=True)

class Item(db.Model):

    id           = db.Column(db.Integer, primary_key=True)
    date         = db.Column(db.Date, nullable=False)
    name         = db.Column(db.String(MAX_NAME_LENGTH), unique=True, nullable=False)
    identifier   = db.Column(db.String(MAX_IDEN_LENGTH), unique=True, nullable=False)
    status       = db.Column(db.String(MAX_STAT_LENGTH), nullable=False)
    category     = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    owner        = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    serialNumber = db.Column(db.String(MAX_SERN_LENGTH), nullable=False)

    
    
