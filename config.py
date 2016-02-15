
import string
import random
import os
_basedir = os.path.abspath(os.path.dirname(__file__))


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Config(object):
    DEBUG = False
    TESTING = True
    DATABASE_URI = 'sqlite:///makeuptest.db'
    SECRET_KEY = "secret" 
    IMAGES = "images/"
    UPLOAD_FOLDER = "/vagrant/itemcatalog/itemcatalog/static/images/"
    ALLOWED_EXTENSIONS = set(['jpg', 'png', 'JPG'])
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    IMAGES_FOLDER = "images/"

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///makeup.db'
    SECRET_KEY = id_generator() 

class DevelopmentConfig(Config):
    DEBUG = True
