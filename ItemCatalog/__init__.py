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

from flask.ext.login import LoginManager

from config import ProductionConfig, DevelopmentConfig
from models import Base

#Create objetcs to use CSRF protection and login managment with flask
csrf = CsrfProtect()
login_manager = LoginManager()

app = Flask(__name__)
csrf.init_app(app)
#login_manager.init_app(app)

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
