#------------------------------------------------------------------------------#
# File: views.py
# Author: Maria Clara De La Cuesta
# Description: Views for the Items Catalog project
#------------------------------------------------------------------------------#
from flask import render_template, url_for, request, redirect, flash
from ItemCatalog import app, session
from models import BodySection, Product
from forms import NewBodySectionForm, NewProductForm


@app.route('/', methods = ['GET','POST'])
def index():
    
    body_sections = session.query(BodySection).order_by(BodySection.name).all()    
    if request.method == 'GET':
        return render_template('index.html', bodysections=body_sections)
        
    if request.method == 'POST':
        
        section_to_delete = (session.query(BodySection).
                            filter(BodySection.id==request.form['id']).one())
        session.delete(section_to_delete)
        session.commit()
        return redirect(url_for('index')) 

@app.route('/section/new/', methods=['GET','POST'])
def newBodySection():

    form = NewBodySectionForm(request.form)
    if request.method == 'GET':
        return render_template('newBodySection.html')
        
    if request.method == 'POST' and form.validate():
        body_section = BodySection()
        form.populate_obj(body_section)
        session.add(body_section)
        session.commit()
        return redirect(url_for('index'))

@app.route('/section/<int:body_section_id>/edit/', methods=['GET','POST']) 
def editBodySection(body_section_id):
    
    form = NewBodySectionForm(request.form) 
    bodysection = (session.query(BodySection).
                    filter(BodySection.id==body_section_id).one())
    if request.method == 'GET':
        return render_template('editBodySection.html', bodysection=bodysection)
        
    if request.method == 'POST' and form.validate():
        form.populate_obj(bodysection)
        session.commit()
        return redirect(url_for('index')) 

 

