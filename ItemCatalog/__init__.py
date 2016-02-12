#------------------------------------------------------------------------------#

# File: _init_.py
# Author: Maria Clara De La Cuesta
# Description:Initialization file for the ItemCatalog server

#------------------------------------------------------------------------------#

from sqlalchemy.orm import sessionmaker
from models import engine, Base
from flask import Flask
from flask_wtf.csrf import CsrfProtect
import os
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

    
class Config(object):
    DEBUG = False
    TESTING = True
    DATABASE_URI = 'sqlite:///makeuptest.db'
    SECRET_KEY = "secret" 
    IMAGES = "images/"

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///makeup.db'
    SECRET_KEY = id_generator() 

class DevelopmentConfig(object):
    DEBUG = True

    
csrf = CsrfProtect()

app = Flask(__name__)
csrf.init_app(app)

app.config['SECRET_KEY'] = id_generator() 
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = "/vagrant/itemcatalog/itemcatalog/static/images/"
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'png', 'JPG'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
IMAGES_FOLDER = "images/"

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

import ItemCatalog.views

''' form.populate_obj(product)
file = request.files['picture']
filename = secure_filename(file.filename)

file.save((app.config['UPLOAD_FOLDER'] + filename))
session.add(product)
session.commit()'''