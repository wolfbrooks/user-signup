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
import webapp2
import re
import cgi


page_header = """
<!DOCTYPE>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

page_footer = """
</body>
</html>
"""
form_signup = """
<form action="/welcome" method="post">
    <label>
        Username:
        <input type="text" name="username">
    </label>
    <br>
    <br>
    <label>
        Password:
        <input type="password" name="password">
    </label>
    <br>
    <br>
    <label>
        Verify Password:
        <input type="password" name="verify">
    </label>
    <br>
    <br>
    <label>
        Email: (optional)
        <input type="text" name="email">
    <br>
    <br>
        <input type="submit" value="Signup!"/>
    </form>
    """

class MainHandler(webapp2.RequestHandler):
    def get(self):
        signup_header = "<h1>Signup</h1>"

        error = self.request.get("error")
        if error:
            error_esc = cgi.escape(error, quote=True)
            error_element = '<p class="error">' + error_esc + '</p>'
        else:
            error_element = ''

        content = page_header + signup_header + form_signup + error_element + page_footer
        self.response.write(content)




class Welcome(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("username")
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        if not USER_RE.match(username):
            error = "Invalid Username"
            self.redirect("/?error=" + error)
        if username == "":
            error = "Please enter a username"
            self.redirect("/?error=" + error)

        password = self.request.get("password")
        verify = self.request.get("verify")
        if password == "":
            error = "Please enter a password"
            self.redirect("/?error=" + error)
        PASS_REGEX = re.compile(r"^.{3,20}$")
        if not PASS_REGEX.match(password):
            error = "Invalid Password"
            self.redirect("/?error=" + error)
        if password != verify:
            error = "Passwords don't match"
            self.redirect("/?error=" + error)

        email = self.request.get("email")
        EMAIL_REGEX = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        if email != "":
            if not EMAIL_REGEX.match(email):
                error = "Invalid Email"
            self.redirect("/?error=" + error)

        welcome_sentance = "Welcome, " + username + "!"
        content = page_header + "<h1>" + welcome_sentance + "</h1>" + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
