#------------------------------------------------------------------------------#

# File: _init_.py
# Author: Maria Clara De La Cuesta
# Description:Initialization file for the ItemCatalog server

#------------------------------------------------------------------------------#

import string
import random
import json
import requests
import httplib2

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask import session as login_session
from flask import make_response

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

<<<<<<< HEAD
from flask.ext.login import LoginManager

=======
>>>>>>> parent of 19e8403... Type: Func Add CSRF protection to the gconnect function, insert CSRF token in the ajaz request
from config import ProductionConfig, DevelopmentConfig
from models import Base

   
csrf = CsrfProtect()
<<<<<<< HEAD
login_manager = LoginManager()
=======
>>>>>>> parent of 19e8403... Type: Func Add CSRF protection to the gconnect function, insert CSRF token in the ajaz request

app = Flask(__name__)
csrf.init_app(app)

app.config.from_object('ItemCatalog.DevelopmentConfig')
#app.config.from_object('ItemCatalog.ProductionConfig')

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']

engine = create_engine(app.config['DATABASE_URI'])
Base.metadata.create_all(engine)

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

import ItemCatalog.views
