#------------------------------------------------------------------------------#
# File: runserver.py
# Author: Maria Clara De La Cuesta
# Description: 
#------------------------------------------------------------------------------#

from ItemCatalog import app
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

app.secret_key = id_generator() 
app.debug = True

app.run(host='0.0.0.0', port=8000)
