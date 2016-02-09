#------------------------------------------------------------------------------#
# File: forms.py
# Author: Maria Clara De La Cuesta
# Description:Forms for the image catalog project
#------------------------------------------------------------------------------#
from wtforms import Form, TextField, IntegerField, validators
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired




class NewBodySectionForm(Form):
    name = TextField('name', [validators.Length(min=4, max=25),
                                validators.Required()])
    description = TextField('description', [validators.Required()])

class NewProductForm(Form):
    name = TextField('name', [validators.Length(min=4, max=25),
                                validators.Required()])
    description = TextField('description', [validators.Required()])
    picture = FileField('picture', [FileAllowed(['jpg'], 'Images only')])
    bodysection_id = IntegerField('maximum_capacity', [validators.Required()])
