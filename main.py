from flask import Flask, request, redirect, render_template
import flask
import re
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

#def build_form(username='', user_error='', password_error='', verify_password='', email='', email_error=''):
#    return """
#form = """
#        
#        """ 

#I need to write code that triggers error if:
# username, pass, or ver pass is empty # username or pass not valid(space, <3 char, >20 char)           
# pass & pass ver don't match # not valid email(can be empty though) must have @ and .
# 

@app.route("/")
def index():
    #template = jinja_env.get_template('index.html')
    return render_template('index.html')

@app.route("/", methods=['POST'])
def signup():

    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''

    #USERNAME 
    #no space in username loop
    i = ""
    for i in username:
        if i.isspace():
            username_error = "Spaces not allowed in username."
    #username length 
    if (len(username)) <3 or (len(username) > 20):
        username_error = "username field must be between 3 & 20 chars"
       
    #if they leave it blank 
    if not username:
        username_error = "username blank"    

    #just a check for now    
    else:
        print ("correct characters username")
    #see if field is empty    

    
    #PASSWORD 
    #no space in password loop
    for i in password:
        if i.isspace():
            password_error = "Spaces not allowed in password."
    #username length 
    if len(password) <3 or len(password) > 20:
        password_error = "username field must be between 3 & 20 chars"
        
    #if they leave it blank 
    if not password:
        password_error = "password blank"    
    #just a check for now    
    else:
        print ("good password entered")
    #see if field is empty    

    #Verify field 
    #only need to check if password and this field match
    if password != verify_password:
        verify_password_error = "Passwords don't match"  
    else:
        print ("correct verify field")
    
    #Email field
    if (email != '') and (not re.match('^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$', email)):
        email_error =("Not a valid email. Include . and @ ")  

#Welcome page if no errors
    if not (username_error or password_error or verify_password_error or email_error):
        return render_template('welcome.html', username=username)
    else:
        print ("had an error")   

      

    return render_template("index.html", username_error=username_error, password_error=password_error,
                        verify_password_error=verify_password_error, email_error=email_error)
            


@app.route("/", methods=['POST'])    
def hello():
    fullname = request.form['username']
    return '<h1> Welcome ' + fullname + '!</h1>'
app.run()   