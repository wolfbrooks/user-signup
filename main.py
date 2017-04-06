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


class MainHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        email = self.request.get("email")
        error2 = self.request.get('error2')
        error1 = self.request.get("error1")
        error3 = self.request.get("error3")
        error4 = self.request.get("error4")
        signup_header = "<h1>Signup</h1>"
        form_signup = """
        <form action="/welcome" method="post">
            <table>
                <tbody>
                    <tr>
                        <td class="label">Username:</td>
                        <td>
                            <input type="text" name="username" value="{0}">
                        </td>
                        <td class="error">{2}
                        </td>
                    </tr>
                    <tr>
                        <td class="label">Password:</td>
                        <td>
                            <input type="password" name="password">
                        </td>
                        <td class="error">{3}
                        </td>
                    </tr>
                    <tr>
                        <td class="label">Verify Password:</td>
                        <td>
                            <input type="password" name="verify">
                        </td>
                        <td class="error">{4}
                        </td>
                    <tr>
                        <td class="label">Email: (optional)</td>
                        <td>
                            <input type="text" name="email" value="{1}">
                        </td>
                        <td class="error">{5}
                        </td>
                    </tr>
                </tbody>
            <table>
            <input type="submit" value="Signup!"/>
        </form>
        """.format(username, email, error1, error2, error3, error4)



        content = page_header + signup_header + form_signup + page_footer
        self.response.write(content)




class Welcome(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")


        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        if not USER_RE.match(username):
            error1 = "Invalid Username"
            self.redirect("/?error1=" + error1)

        PASS_REGEX = re.compile(r"^.{3,20}$")
        if not PASS_REGEX.match(password):
            error2 = "Invalid Password"
            self.redirect("/?error2=" + error2)

        if password != verify:
            error3 = "Passwords don't match"
            self.redirect("/?error3=" + error3)

        EMAIL_REGEX = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        if email != "":
            if not EMAIL_REGEX.match(email):
                error4 = "Invalid Email"
            self.redirect("/?error4=" + error4)

        welcome_sentance = "Welcome, " + username + "!"
        content = page_header + "<h1>" + welcome_sentance + "</h1>" + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
