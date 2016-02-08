#------------------------------------------------------------------------------#
# File: views.py
# Author: Maria Clara De La Cuesta
# Description: Views for the puppy shelter project
#------------------------------------------------------------------------------#
from flask import render_template, url_for, request, redirect, flash
from ItemCatalog import app#, session
#from models import BodySection, Product
#from forms import NewBodySectionForm, NewProductForm


@app.route('/')
def index():
        
    if request.method == 'GET':
        return render_template('index.html')
        
    if request.method == 'POST' and form.validate():  
        return redirect(url_for('index')) 

@app.route('/section/new/', methods=['GET','POST'])
def newBodySection():
    #form = NewShelterForm(request.form)
    if request.method == 'GET':
        return render_template('newBodySection.html')
        
    if request.method == 'POST' and form.validate():
        return redirect(url_for('index'))


@app.route('/section/<int:section_id>/edit/', methods=['GET','POST'])
def edit_body_section(section_id):

    if request.method == 'GET':
        return render_template('editBodySection.html', shelter=shelter)
        
    if request.method == 'POST' and form.validate():  
        return redirect(url_for('index')) 


@app.route('/products/', methods=['GET','POST'])
def list_products():
    if request.method == 'GET':
        return render_template('products.html')
        
    if request.method == 'POST' and form.validate():  
        return redirect(url_for('list_products')) 

@app.route('/products/new/', methods=['GET','POST'])
def new_product():
    #form = NewShelterForm(request.form)
    if request.method == 'GET':
        return render_template('newProduct.html')
        
    if request.method == 'POST' and form.validate():
        return redirect(url_for('list_products'))
        
        
@app.route('/products/<int:product_id>/edit/', methods=['GET','POST'])
def edit_product(product_id):
    if request.method == 'GET':
        return render_template('editProduct.html', shelter=shelter)
        
    if request.method == 'POST' and form.validate():  
        return redirect(url_for('list_products')) 

 

