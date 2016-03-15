#------------------------------------------------------------------------------#
# File: Models.py
# Author: Maria Clara De La Cuesta
# Description: models for the item catalog project
#------------------------------------------------------------------------------#

from sqlalchemy import (Column, ForeignKey, Integer, String, Date, Boolean, 
    Numeric,Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class BodySection(Base):
    __tablename__ = 'bodysection'
    
    name = Column(String(80), nullable = False)
    description =  Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    
    def __repr__(self):
        return ("Body Part [N:%s \n D: %s]>" % (self.name, self.description))
        
    @property
    def serialize(self):
        #Return objetcs in an easily serializable format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id
        }
               
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

    @property
    def serialize(self):
        #Return objetcs in an easily serializable format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'body_picture' : self.picture_name,
            'bodysection_id' : self.bodysection_id 
        }
 
class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    name = Column(String(80))
    email = Column(String(80)) 
    picture = Column(String)
    authenticated = Column(Boolean)
    
    def __init__(self, username, email, picture, authenticated):
        self.name = username
        self.email = email
        self.picture = picture
        self.authenticated = authenticated
    
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    def __repr__(self):
        return ("<User [N:'%s' \n 'E:'%s' \n A:'%s']>" % (self.name, 
            self.email, self.authenticated))
    

                

