from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ministry(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(240))
    items = db.relationship('Item', backref='ministry', lazy=True)

class Storage(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    location = db.Column(db.String(240), nullable=False)
    items = db.relationship('Item', backref='storage', lazy=True)

class Category(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(240), nullable=False)
    items = db.relationship('Item', backref='category', lazy=True)

class Status(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(240), nullable=False)
    items = db.relationship('Item', backref='status', lazy=True)

class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(24), nullable=False)
    
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministry.id'), nullable=False)
    storage_id = db.Column(db.Integer, db.ForeignKey('storage.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    
