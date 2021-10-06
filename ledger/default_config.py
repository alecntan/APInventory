import os

basedir = os.path.abspath(os.path.dirname(__file__))

TESTING=False
DEBUG=True
FLASK_ENV='development'
DATABASE = os.path.join(basedir, "../ledger.sqlite")
SQLALCHEMY_DATABASE_URI='sqlite:///' + DATABASE
SQLALCHEMY_TRACK_MODIFICATIONS=False


