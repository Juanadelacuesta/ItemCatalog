#Item Catalog Web App

Third project for the Udacity full Stack Nano Degree

This project consists in the development of a full functional RESTfull 
application user registration and authentication system. Registered users
will have the ability to post, edit and delete their own items.  
To run this application you need to install 

The application uses SQLAlchemy, Flask-SQLAlchemy, Flask-WTF, FLask-OAuth and 
Flask-Login. In order to make it work you may also need httplib2, json,
requests, os, urllib2 and werkzeug libraries. 

It has two possible configurations, Development and Production, to chose, go
to the __init__.py file and comment the setup you are not going to use.

For the Google Authentication system to work you need to get user credentials 
from the google console, you can find the information to do it in this [link]
(https://developers.google.com/identity/protocols/OAuth2).
Once you get the client secret json file, save it in the same file as the 
runserver.py file under the name client_secret.json 

To run it just execute the runserver.py file.

 
##Contents 

The structure of the project is as follows:

ItemCatalog/
 * runserver.py
 * config.py
 * ReadMe.md  
 * ItemCatalog/
  * \__init\__.py
  * models.py
  * views.py
  * templates/
   * static/
   * style.css
    * images/
