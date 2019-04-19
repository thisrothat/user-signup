#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import flask
import cgi
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <link type="text/css" rel="stylesheet" href="css/normalize.css">
    <link type="text/css" rel="stylesheet" href="css/styles.css">
    <title>User Sign-Up</title>
</head>
<body>
    <h1>
        User Sign-Up
    </h1>
"""
page_header_welcome = """
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <link type="text/css" rel="stylesheet" href="normalize.css">
    <link type="text/css" rel="stylesheet" href="css/styles_wel.css">
    <title>Welcome!</title>
</head>
<body id='wel'>
    <h1>
        <img src='http://itemsforsalebycallkeithcustomers.homestead.com/files/WelcomeSignStaredAnimated.gif'/>
    </h1>
"""
page_footer = """
</body>
<footer>
    <address>
        <p><br>Contents written by: <span id='myname'><b>Brittani Luce</b></span></p>
        <p>Written for: LaunchCode 101 -- User Sign-Up
        <p>Thank you for visiting!</p>
    </address>
        <p id='copy'>&#169;Brittani Luce, 2017
        <br><br></p>
</footer>
</html>
"""

def build_form(username='', user_error='', password_error='', verify_password='', email='', email_error=''):
    return """
        <div>
        <form method='post'>
        	<p><label id='user'>*Username*: </label>
        	<input id='userin' type='text' name='user' value={username}></input></p>
        	<p><span class="error">{user_error}</span></p>
        	<p><label id='pass'>*Password*: </label>
        	<input id='passin' type='password' name='password'/></p>
        	<p><span class="error">{password_error}</span></p>
        	<p><label id='verif'>*Verify Password*: </label>
        	<input id='verifin' type='password' name='verify'/></p>
        	<p><span class="error">{verify_password}</span></p>
        	<p><label id='em'>Email: </label>
        	<input id='emin' type='text' name='email' value={email}></input></p>
        	<p><span class="error">{email_error}</span></p>
            <br>
            <p><span id='req'>*Required Information*</span></p>
        	<p><input type='submit' value='Let&apos;s&nbsp;Go!'/>
            <br>
            <br>
            <button value='clear'><a id='clear' href='/'>Clear the Form</a></button></p>
        </form>
        </div>
        """.format(username=username, user_error=user_error, password_error=password_error,
            verify_password=verify_password, email=email, email_error=email_error)

def valid_username(user_input):
    """Checks if the username input is valid."""
    user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return user_re.match(user_input)

def valid_password(password_input):
    """Checks if the password input is valid."""
    password_re = re.compile(r"^.{3,20}$")
    return password_re.match(password_input)

def valid_email(email_input):
    """Checks if ther is email input. If there is, checks if it is valid."""
    if email_input == "":
        return True
    else:
        email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        return email_re.match(email_input)

def password_verified(password_input, verify_input):
    """Checks if the Password and Verify Password fields match."""
    if password_input == verify_input:
        return True
    else:
        return False

class MainHandler(flask.RequestHandler):
    def get(self):
        """First page that the user comes to. Handles the first GET request."""
        self.response.write(page_header + build_form() + page_footer)

    def post(self):
        username = self.request.get("user")
        user_esc = cgi.escape(username, quote=True)
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        fail = False

        if user_esc == "":
            username_error = "You must enter a Username!"
            fail = True
        elif " " in user_esc:
            username_error = "Username cannot contain spaces!"
            fail = True
        elif not valid_username(user_esc):
            username_error = "Please enter a valid Username!"
            fail = True
        else:
            username_error = ""

        if not valid_password(password):
            password_error = "Please enter a valid Password!"
            fail = True
        else:
            password_error = ""

        if not password_verified(password, verify):
            verify_error = "Password fields must match!"
            fail = True
        else:
            verify_error = ""

        if not valid_email(email):
            email_error = "Please enter a valid Email!"
            fail = True
        else:
            email_error = ""

        if fail:
            self.response.write(page_header + build_form(username=user_esc, user_error=username_error,
            password_error=password_error, verify_password=verify_error, email=email,
            email_error=email_error) + page_footer)
        else:
            self.redirect("/welcome?username={}&email={}".format(user_esc, email))


class Welcome(webapp2.RequestHandler):
    """Handles requests coming into '/welcome'."""
    def get(self):
        user = self.request.get("username")
        email = self.request.get("email")
        if email == "":
            email = "<em>No email provided.</em>"
        user = "<span id='user'><strong>" + user + "</span></strong>"
        email = "<strong>" + email + "</strong>"
        welcome = "Hello %s, thank you for signing up!" % user
        message = "Watch for your welcome email soon!"
        welcome_element = "<p class='welcome'>" + welcome
        message_element = "<br>" + message + "<br><br><br>Email:  " + email + "</p>"
        welcome_content = page_header_welcome + welcome_element + message_element + page_footer
        self.response.write(welcome_content)

app = flask.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
    ])

