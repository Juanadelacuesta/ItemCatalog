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

csrf = CsrfProtect()
UPLOAD_FOLDER = "/vagrant/itemcatalog/itemcatalog/images/"

app = Flask(__name__)
csrf.init_app(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'png'])

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