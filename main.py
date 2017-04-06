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
signup_header = "<h1>Signup</h1>"
form_signup = """
<form method="post">
    <table>
        <tbody>
            <tr>
                <td class="label">Username:</td>
                <td>
                    <input type="text" name="username" value="%(username)s">
                </td>
                <td class="error">%(error_user)s
                </td>
            </tr>
            <tr>
                <td class="label">Password:</td>
                <td>
                    <input type="password" name="password">
                </td>
                <td class="error">%(error_pass)s
                </td>
            </tr>
            <tr>
                <td class="label">Verify Password:</td>
                <td>
                    <input type="password" name="verify">
                </td>
                <td class="error">%(error_verify)s
                </td>
            <tr>
                <td class="label">Email: (optional)</td>
                <td>
                    <input type="text" name="email" value="%(email)s">
                </td>
                <td class="error">%(error_email)s
                </td>
            </tr>
        </tbody>
    <table>
    <input type="submit" value="Signup!"/>
</form>
"""

class MainHandler(webapp2.RequestHandler):
    def writeForm(self, error_user="", error_pass="", error_verify="", error_email="", username="", email=""):
        content = page_header + signup_header + form_signup + page_footer
        self.response.out.write(content %{"error_user": error_user, "error_pass": error_pass, "error_verify":error_verify, "error_email":error_email, "username":username, "email":email})

    def get(self):
        self.writeForm()


    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        hasError = False
        perams = {"username":username, "email":email}
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        if not USER_RE.match(username):
            perams['error_user'] = "Invalid Username"
            hasError = True

        PASS_REGEX = re.compile(r"^.{3,20}$")
        if not PASS_REGEX.match(password):
            perams['error_pass'] = "Invalid Password"
            hasError = True

        if password != verify:
            perams['error_verify'] = "Passwords don't match"
            hasError = True

        EMAIL_REGEX = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        if email != "":
            if not EMAIL_REGEX.match(email):
                perams['error_email'] = "Invalid Email"
                hasError = True

        if hasError:
            self.writeForm(**perams)
        else:
            self.redirect("/welcome?username=" + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")

        welcome_sentance = "Welcome, " + username + "!"
        content = page_header + "<h1>" + welcome_sentance + "</h1>" + page_footer
        self.response.out.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
