#------------------------------------------------------------------------------#
# File: views.py
# Author: Maria Clara De La Cuesta
# Description: Views for the Items Catalog project
#------------------------------------------------------------------------------#
import httplib2
import json
import requests
import os

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError


from flask import render_template, url_for, request, redirect, flash, jsonify
from flask import make_response
from flask import session as login_session
from urllib2 import urlopen
from werkzeug import secure_filename
from flask_wtf.file import FileField
from sqlalchemy_imageattach.context import store_context


from config import id_generator
from ItemCatalog import app, session, csrf, CLIENT_ID
from models import BodySection, Product
from forms import NewBodySectionForm, NewProductForm

'''Function to check if the user is uploading an accepted image file
    It recives the file name, extention included
    It returns:
    True if the file is valid
    False if not
'''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    

@app.route('/login')
def showLogin():
        state = id_generator(32) 
        login_session['state'] = state
        return render_template('login.html', STATE = state)
 
@csrf.exempt
@app.route('/gconnect', methods=['POST'])
def gconnect():

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter blah'), 401)
        response.headers['Content-Type']  = 'aplication/json'
        return response
    
    # Obtain authorization code

    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='') 
        oauth_flow.redirect_uri='postmessage'
        credentials = oauth_flow.step2_exchange(code)
        
    except FlowExchangeError:
        print "dentro de error"
        response = make_response(json.dumps('Failed to upgrade the' + 
        'authorization code blah'), 401)
        response.headers['Content-Type']  = 'aplication/json'
        return response
    
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
            % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    
    #If the access token is invalid, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user Id doesnt match"), 401)
        response.headers['Content-Type']  = 'aplication/json'
        return response
        
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's blah."
        response.headers['Content-Type'] = 'application/json'
        return response
    
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    
    
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
   
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 150px; height: 150px;border-radius: 75px;' 
    output += '-webkit-border-radius: 75px;-moz-border-radius: 75px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output
    
@app.route('/')
@app.route('/section/')
def index():

    body_sections = session.query(BodySection).order_by(BodySection.name).all()    
    print login_session['picture']
    return render_template('index.html', bodysections=body_sections, image=login_session['picture'])

    
@app.route('/section/<int:section_id>/')
def section(section_id):
    
    body_section = (session.query(BodySection).
        filter(BodySection.id==section_id).one()) 
    products = (session.query(Product).filter(Product.bodysection_id==section_id)
                    .all())  
    if request.method == 'GET': 
        return render_template('section.html', bodysection=body_section, 
                                    products=products)
        
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
        
        elif request.form['btn'] == 'Cancel':
            return redirect(url_for('section', section_id=body_section_id))

        
# Views for the Products

@app.route('/product/')
def viewProducts():
    
    products = session.query(Product).order_by(Product.bodysection_id).all()    
    return render_template('products.html', products=products)
 

@app.route('/product/new/<int:section_id>', methods=['GET','POST'])
@app.route('/product/new/', methods=['GET','POST'])
def newProduct(section_id=None):
    
    sections = session.query(BodySection).all()
    if section_id:
        preselected_section = (session.query(BodySection).
                                    filter(BodySection.id==section_id).one())
    else:
        preselected_section = section_id
        
    form = NewProductForm(request.form)
    product = Product()
    if request.method == 'GET':
        return render_template('newProduct.html', sections=sections,
                                ps_section=preselected_section)
        
    if request.method == 'POST' and form.validate():       
        form.populate_obj(product)
        file = request.files['picture']
        filename = secure_filename(file.filename)
        product.picture_name = app.config['IMAGES_FOLDER'] + filename
        if allowed_file(filename):
            file.save(app.config['UPLOAD_FOLDER'] + filename)
            session.add(product)
            session.commit()
            
        if section_id:
            return redirect(url_for('section', section_id=section_id))
            
        return redirect(url_for('viewProducts'))    

@app.route('/product/<int:product_id>/')
def product(product_id):
    
    product = (session.query(Product).
        filter(Product.id==product_id).one()) 
        
    if request.method == 'GET': 
        return render_template('product.html', product=product)

@app.route('/product/<int:product_id>/edit/', methods=['GET','POST']) 
def editProduct(product_id):
    
    form = NewProductForm(request.form)
    product = (session.query(Product).
                    filter(Product.id==product_id).one())
    sections = session.query(BodySection).all()                
    if request.method == 'GET':
        return render_template('editProduct.html', 
                                product=product, sections= sections)

    if request.method == 'POST' and form.validate():
        print '/n/n/n/ post/n/n'
        if request.form['btn'] == 'Save':
            form.populate_obj(product)           
            if request.files['picture']:
                file = request.files['picture']
                filename = secure_filename(file.filename)
                product.picture_name = IMAGES_FOLDER + filename
                file.save(app.config['UPLOAD_FOLDER'] + filename)
                session.add(product)
                session.commit()
            return redirect(url_for('product', product_id=product_id)) 
            
        elif request.form['btn'] == 'Cancel':
            return redirect(url_for('product', product_id=product_id))    
            
@app.route('/product/<int:product_id>/delete/', methods=['GET','POST']) 
def deleteProduct(product_id):
     
    product = (session.query(Product).
                    filter(Product.id==product_id).one())
    form = NewProductForm(request.form)
    if request.method == 'GET':
        return render_template('deleteProduct.html', product=product)
        
    if request.method == 'POST':
        if request.form['btn'] == 'Delete':
            session.delete(product)
            session.commit()
        return redirect(url_for('viewProducts'))
        
@app.route('/section/<int:section_id>/JSON/')
def bodySectionJson(section_id):
    section = session.query(BodySection).filter_by(id=section_id).one()
    products = session.query(Product).filter_by(bodysection_id=section.id)
    return jsonify(specific_products=[p.serialize for p in products])

@app.route('/product/<int:product_id>/JSON/')
def productJson(product_id):
    product = session.query(Product).filter_by(id=product_id).one()
    return jsonify(Product_info=product.serialize)
