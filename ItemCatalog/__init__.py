#------------------------------------------------------------------------------#

# File: _init_.py
# Author: Maria Clara De La Cuesta
# Description:Initialization file for the ItemCatalog server

#------------------------------------------------------------------------------#

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask import session as login_session
import string
import random
from config import ProductionConfig, DevelopmentConfig
from models import Base

   
csrf = CsrfProtect()

app = Flask(__name__)
csrf.init_app(app)

app.config.from_object('ItemCatalog.DevelopmentConfig')
#app.config.from_object('ItemCatalog.ProductionConfig')


engine = create_engine(app.config['DATABASE_URI'])
Base.metadata.create_all(engine)

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

import ItemCatalog.views
