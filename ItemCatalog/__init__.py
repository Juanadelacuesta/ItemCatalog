#------------------------------------------------------------------------------#

# File: _init_.py
# Author: Maria Clara De La Cuesta
# Description:Initialization file for the ItemCatalog server

#------------------------------------------------------------------------------#

from sqlalchemy.orm import sessionmaker
from models import Base
from sqlalchemy import create_engine
from flask import Flask
from flask_wtf.csrf import CsrfProtect
from config import ProductionConfig, DevelopmentConfig

   
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
