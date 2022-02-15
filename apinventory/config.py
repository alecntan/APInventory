from flask import Flask

class Default:

    DATABASE_PATH='/tmp/test.db'
    SQLALCHEMY_DATABASE_URI='sqlite:///{}'.format(DATABASE_PATH)
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    CORS_EXPOSE_HEADERS=['message', 'error']
