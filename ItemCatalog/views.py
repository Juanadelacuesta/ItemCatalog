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
from flask_wtf.file import FileField
from flask.ext.login import login_required

from urllib2 import urlopen
from werkzeug import secure_filename
from sqlalchemy_imageattach.context import store_context
import psycopg2

from config import id_generator
from ItemCatalog import app, session, csrf, CLIENT_ID, login_manager
from models import BodySection, Product, User
from forms import NewBodySectionForm, NewProductForm

'''
    Function to save a new user to the database
    Receives a flask login_session object
    Returns the newly saved user's id or None if it was not saved
'''
def createUser(login_session):

    try:
        user = User(login_session['username'], 
                    login_session['email'], 
                    login_session['picture'],
                    True)
                    
        session.add(user)
        session.commit()
        user = session.query(User).filter_by(email=login_session['email']).one()
        return user.id   
    
    except:
        return None
 
'''
    Function to given *user_id*, return the associated User object.
    Recieves: The user email
    Returns: The user object retrived from the database or None if the
        user doesn't exist.
''' 
@login_manager.user_loader
def user_loader(user_email):
    
    try:
        return session.query(User).filter(User.email==user_email).one()
    
    except:
        return None

'''
    Function to check if the user is uploading an accepted image file
    It recieves the file name, extention included
    It returns:
    True if the file is valid
    False if not
'''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    
'''
    Function to create http response
    It recieves, the text to show and the error code
    It returns the response
'''
def create_http_response(response_text, response_code):
        response = make_response(json.dumps(response_text, response_code))
        response.headers['Content-Type']  = 'application/json'
        return response
       
# Log in page
@app.route('/login')
def showLogin():
        state = id_generator(32) 
        login_session['state'] = state
        return render_template('login.html', STATE = state)
 
 
# CONNECT - Identify de user using the google oauth API  
<<<<<<< HEAD
=======
@csrf.exempt
>>>>>>> parent of 19e8403... Type: Func Add CSRF protection to the gconnect function, insert CSRF token in the ajaz request
@app.route('/gconnect', methods=['POST'])
def gconnect():

    if request.args.get('state') != login_session['state']:
        return create_http_response('Invalid state parameter', 401)
    
    # Obtain authorization code
    code = request.data
    
    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='') 
        oauth_flow.redirect_uri='postmessage'
        credentials = oauth_flow.step2_exchange(code)
        
    except FlowExchangeError:
        return create_http_response('Failed to upgrade the authorization code' +
                                    'blah', 401)
    
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
            % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    
    #If the access token is invalid, abort
    if result.get('error') is not None:
        return create_http_response(result.get('error'), 500)
        
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return create_http_response("Token's user Id doesnt match", 401)
        
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        print "Token's client ID does not match app's."
        return create_http_response("Token's client ID does not match app's.", 
                                    401)
   
    # Verify the user is not already connected
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return create_http_response('Current user is already connected', 200)
        
    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    
    
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    
    #Save user info for the session
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    
    #Check if the user existe in the database and save
    if user_loader(login_session['email']) is None: 
        login_session['user_id'] = createUser(login_session)
    
    else:
        login_session['user_id'] = user_loader(login_session['email']).id

    #Display welcome page
    flash("you are now logged in as %s" % login_session['username'])
    return render_template('loginsucces.html', 
                            username=login_session['username'], 
                            picture=login_session['picture'])
 
# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():

    #Get current session credentials
    access_token = login_session['access_token']
    print 'The user to be disconnected is: ' 
    print login_session['username']
    
    #If there is no current active user
    if access_token is None:
 	print 'Access Token is None'
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    
    if result['status'] == '200':
        del login_session['access_token'] 
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
        flash('Successfully disconnected')
    	return redirect(url_for('showLogin'))
   
    else:
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response
    
# Index page
@login_required
@app.route('/')
@app.route('/section/')
def index():
    
    if 'username'  in login_session:
        picture = login_session['picture']
    else:
        picture = None
        
    body_sections = session.query(BodySection).order_by(BodySection.name).all()
    
    return render_template('index.html', bodysections=body_sections, 
        image=picture)

# Page of a specific body section  
@app.route('/section/<int:section_id>/')
def section(section_id):
     
    try:
        if 'username'  in login_session:
            picture = login_session['picture']
        else:
            picture = None
            
        body_section = (session.query(BodySection).
            filter(BodySection.id==section_id).one()) 
    
        products = (session.query(Product).filter(Product.bodysection_id==section_id)
                    .all())  
        if request.method == 'GET': 
            return render_template('section.html', bodysection=body_section, 
                                    products=products,
                                    image=login_session['picture'])
    
    except:
        flash("That particular section is not defined ")
        return redirect(url_for('newBodySection'))

# Page to add a new body section          
@app.route('/section/new/', methods=['GET','POST'])
def newBodySection():
    
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
        
    form = NewBodySectionForm(request.form)
    if request.method == 'GET':
        return render_template('newBodySection.html',
            image=login_session['picture'])
        
    if request.method == 'POST' and form.validate():
        body_section = BodySection()
        form.populate_obj(body_section)
        body_section.user_id = login_session['user_id'] 
        session.add(body_section)
        session.commit()
        return redirect(url_for('index'))

# Page to edit a specific body section         
@app.route('/section/<int:body_section_id>/edit/', methods=['GET','POST']) 
def editBodySection(body_section_id):
    
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    
    try:
        form = NewBodySectionForm(request.form)
        body_section = (session.query(BodySection).
                        filter(BodySection.id==body_section_id).one())
                        
        if request.method == 'GET':
            return render_template('editBodySection.html', bodysection=body_section,
                                    image=login_session['picture'])

        if request.method == 'POST' and form.validate():
        
            if request.form['btn'] == 'Update':
                form.populate_obj(body_section)
                session.commit()
                return redirect(url_for('index')) 
                
            elif request.form['btn'] == 'Cancel':
                return redirect(url_for('section', section_id=body_section_id))        

    except:
        flash("That particular section is not defined ")
        return redirect(url_for('newBodySection'))
 
# Page to delete a body section 
@app.route('/section/<int:body_section_id>/delete/', methods=['GET','POST']) 
def deleteBodySection(body_section_id):
    
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    
    try:
        body_section = (session.query(BodySection).
                        filter(BodySection.id==body_section_id).one())
        form = NewBodySectionForm(request.form)
        if request.method == 'GET':
            return render_template('deleteBodySection.html', 
                                    bodysection=body_section,
                                    image=login_session['picture'])
            
        if request.method == 'POST':
            if request.form['btn'] == 'Delete':
                session.delete(body_section)
                session.commit()
                return redirect(url_for('index'))
            
            elif request.form['btn'] == 'Cancel':
                return redirect(url_for('section', section_id=body_section_id))

    except:
        flash("That particular section is not defined ")
        return redirect(url_for('newBodySection'))    

# Views for the Products
# Page to list all products ordered by section
@app.route('/product/')
def viewProducts():
    
    products = session.query(Product).order_by(Product.bodysection_id).all()    
    return render_template('products.html', products=products,
                            image=login_session['picture'])
 

@app.route('/product/new/<int:section_id>', methods=['GET','POST'])
@app.route('/product/new/', methods=['GET','POST'])
def newProduct(section_id=None):
    
    if 'username'  in login_session:
        picture = login_session['picture']
    else:
        picture = None
    
    sections = session.query(BodySection).all()
    
    # Check if the request comes from a particular section 
    if section_id:
        preselected_section = (session.query(BodySection).
                                    filter(BodySection.id==section_id).one())
    else:
        preselected_section = section_id
        
    form = NewProductForm(request.form)
    product = Product()
    if request.method == 'GET':
        return render_template('newProduct.html', sections=sections,
                                ps_section=preselected_section,
                                image=login_session['picture'])
        
    if request.method == 'POST' and form.validate():       
        form.populate_obj(product)
        file = request.files['picture']
        filename = secure_filename(file.filename)
        product.user_id = login_session['user_id']
        product.picture_name = app.config['IMAGES_FOLDER'] + filename 
        if allowed_file(filename):
            file.save(app.config['UPLOAD_FOLDER'] + filename)
            session.add(product)
            session.commit()
        else:
            flash("Error while saving the photo file!")
        if section_id:
            return redirect(url_for('section', section_id=section_id))
            
        return redirect(url_for('viewProducts'))    

# Page to view the information on a specific product
@app.route('/product/<int:product_id>/')
def product(product_id):
    
    if 'username'  in login_session:
        picture = login_session['picture']
    else:
        picture = None
    
    try:
        product = (session.query(Product).
            filter(Product.id==product_id).one()) 
            
        if request.method == 'GET': 
            return render_template('product.html', product=product,
                                    image=login_session['picture'])
    
    except:
        flash("That particular product is not defined ")
        return redirect(url_for('newProduct'))    

# Page to edit a specific product
@app.route('/product/<int:product_id>/edit/', methods=['GET','POST']) 
def editProduct(product_id):
    
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
        
    try:
        form = NewProductForm(request.form)
        product = (session.query(Product).
                        filter(Product.id==product_id).one())
        sections = session.query(BodySection).all()                
        if request.method == 'GET':
            return render_template('editProduct.html', 
                                    product=product, sections= sections,
                                    image=login_session['picture'])

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
    except:
        flash("That particular product is not defined ")
        return redirect(url_for('newProduct'))    
                

# Page to delete a specific product
@app.route('/product/<int:product_id>/delete/', methods=['GET','POST']) 
def deleteProduct(product_id):
    
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    
    try:
        product = (session.query(Product).
                        filter(Product.id==product_id).one())
        form = NewProductForm(request.form)
        if request.method == 'GET':
            return render_template('deleteProduct.html', product=product,
                                    image=login_session['picture'])
            
        if request.method == 'POST':
            if request.form['btn'] == 'Delete':
                session.delete(product)
                session.commit()
            return redirect(url_for('viewProducts'))
    except:
        flash("That particular product is not defined ")
        return redirect(url_for('newProduct'))    
 
# Get a body section information in json format 
@app.route('/section/<int:section_id>/JSON/')
def bodySectionJson(section_id):
    try:
        section = session.query(BodySection).filter_by(id=section_id).one()
        products = session.query(Product).filter_by(bodysection_id=section.id)
        return jsonify(specific_products=[p.serialize for p in products])
    except: 
        return (json.dumps(''))
 
# Get a product information in json format  
@app.route('/product/<int:product_id>/JSON/')
def productJson(product_id):
    try:
        product = session.query(Product).filter_by(id=product_id).one()
        return jsonify(Product_info=product.serialize)
    except:
        return (json.dumps(''))
        