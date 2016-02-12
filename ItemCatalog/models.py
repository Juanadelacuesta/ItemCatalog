#------------------------------------------------------------------------------#
# File: Models.py
# Author: Maria Clara De La Cuesta
# Description: models for the item catalog project
#------------------------------------------------------------------------------#

from sqlalchemy import (Column, ForeignKey, Integer, String, Date, Enum, 
    Numeric,Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class BodySection(Base):
    __tablename__ = 'bodysection'
    
    name = Column(String(80), nullable = False)
    description =  Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    
    def __repr__(self):
        return ("Body Part [N:%s \n D: %s]>" % (self.name, self.description))

               
class Product(Base):

    __tablename__ = 'product' 
    id = Column(Integer, primary_key = True)    
    name = Column(String(80), nullable = False)
    description = Column(String(150)) 
    picture_name = Column(String(30))
    bodysection_id = Column(Integer, ForeignKey('bodysection.id'))
    bodysection = relationship('BodySection')
    
    def __repr__(self):
        return ("<Product [N:'%s' \n 'D:'%s' \n BS:'%s' PP: %s ]>" % (self.name, 
                self.description, self.bodysection, self.picture_name))
    
    
engine = create_engine('sqlite:///makeup.db')
Base.metadata.create_all(engine)

