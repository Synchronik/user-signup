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

form="""
<form method="post">

<h1>Sign-Up</h1>

<label>Username
    <input type="text" name="name" value=%(name)s>
</label>

<div style="color: red">%(errora)s</div>

<br>

<label>Password
    <input type="password" name="pas" value=%(pas)s>
</label>

<div style="color: red">%(errorb)s</div>

<br>

<label>Verify Password
    <input type="password" name="vpass" value=%(vpass)s>
</label>

<div style="color: red">%(errorc)s</div>

<br>

<label>Email (Optional)
    <input type="text" name="email" value=%(email)s>
</label>

<div style="color: red">%(errord)s</div>

<br>
<br>
<input type="submit">
</form>
"""


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validName(name):
    return name and USER_RE.match(name)

PASS_RE = re.compile(r"^.{3,20}$")
def validPassword(paz):
    return paz and PASS_RE.match(paz)

def validVpassword(x,y):
    if x == y:
        return True
    else:
        return False

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def validEmail(mel):
    return not mel or EMAIL_RE.match(mel)


class MainHandler(webapp2.RequestHandler):
    def writeForm(self,errora="",errorb="",errorc="",errord="", name="", pas="", vpass="", email=""):
        self.response.out.write(form % {"errora": errora,
                                        "errorb": errorb,
                                        "errorc": errorc,
                                        "errord": errord,
                                        "name": name,
                                        "pas": pas,
                                        "vpass": vpass,
                                        "email": email
                                                    })

    def get(self):
        self.writeForm()

    def post(self):
        haveError = False
        username = self.request.get('name')
        password = self.request.get('pas')
        vpassword = self.request.get('vpass')
        email = self.request.get('email')

        user = validName(username)
        pw = validPassword(password)
        vpw = validVpassword(password,vpassword)
        mail = validEmail(email)

        if not user:
            haveError = True
            a="Invalid username"
        else:
            a=""

        if not pw:
            haveError = True
            b="Invalid password"
        else:
            b=""

        if vpw == False:
            haveError = True
            c="Passwords do not match"
        else:
            c=""

        if not mail:
            haveError = True
            d = "Invalid email"
        else:
            d=""

        if haveError == True:
            self.writeForm(a,b,c,d,username,"","",email)
        else:
            self.response.out.write("Welcome, " + username + "!")


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
