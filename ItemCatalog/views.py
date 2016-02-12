#------------------------------------------------------------------------------#
# File: views.py
# Author: Maria Clara De La Cuesta
# Description: Views for the Items Catalog project
#------------------------------------------------------------------------------#
from flask import render_template, url_for, request, redirect, flash
from urllib2 import urlopen
from werkzeug import secure_filename
from flask_wtf.file import FileField
import os
from sqlalchemy_imageattach.context import store_context
from ItemCatalog import app, session

from models import BodySection, Product

from forms import NewBodySectionForm, NewProductForm

IMAGES_FOLDER = "images/"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    

@app.route('/')
@app.route('/section/')
def index():
    body_sections = session.query(BodySection).order_by(BodySection.name).all()    
    return render_template('index.html', bodysections=body_sections)

    
@app.route('/section/<int:section_id>/')
def section(section_id):
    
    body_section = (session.query(BodySection).
        filter(BodySection.id==section_id).one()) 
        
    if request.method == 'GET': 
        return render_template('section.html', bodysection=body_section)
        
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
    body_section = (session.query(BodySection).
                    filter(BodySection.id==body_section_id).one())
    if request.method == 'GET':
        return render_template('editBodySection.html', bodysection=body_section)

    if request.method == 'POST' and form.validate():
    
        if request.form['btn'] == 'Save':
            form.populate_obj(body_section)
            session.commit()
            return redirect(url_for('index')) 
            
        elif request.form['btn'] == 'Cancel':
            return redirect(url_for('section', section_id=body_section_id))        

@app.route('/section/<int:body_section_id>/delete/', methods=['GET','POST']) 
def deleteBodySection(body_section_id):
     
    body_section = (session.query(BodySection).
                    filter(BodySection.id==body_section_id).one())
    form = NewBodySectionForm(request.form)
    if request.method == 'GET':
        return render_template('deleteBodySection.html', bodysection=body_section)
        
    if request.method == 'POST':

        if request.form['btn'] == 'Delete':
            session.delete(body_section)
            session.commit()
        return redirect(url_for('index'))
 #   print '\n salio \n\n'

        
# Views for the Products

@app.route('/product/')
def viewProducts():
    
    products = session.query(Product).order_by(Product.bodysection_id).all()    
    return render_template('products.html', products=products)
        
@app.route('/product/new/', methods=['GET','POST'])
def newProduct():
 
    form = NewProductForm(request.form)
    product = Product()
    if request.method == 'GET':
        return render_template('newProduct.html')
        
    if request.method == 'POST' and form.validate():       
        form.populate_obj(product)
        file = request.files['picture']
        filename = secure_filename(file.filename)
        product.picture_name = IMAGES_FOLDER + filename
        print "\n\n"
        print product
        print "\n\n"
        if allowed_file(filename):
            print "\n\n"+ product.picture_name +"\n\n\n"
            file.save(app.config['UPLOAD_FOLDER'] + filename)
            session.add(product)
            session.commit()
        return redirect(url_for('viewProducts'))


