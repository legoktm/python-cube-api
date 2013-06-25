#!/usr/bin/env python
"""
Copyright (C) 2013 Legoktm

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import cgitb
cgitb.enable()
import cgi
import json
import os
import requests
import yaml

url = 'http://stats.wmflabs.org:83/thing'


def die(code, message):
    print json.dumps({'error': {'code': code, 'message': message}})
    quit()

with open('~/.access.yml', 'r') as f:
    access = yaml.load(f)

#Check if POST
if os.environ['REQUEST_METHOD'].lower() != 'post':
    die('mustpost', 'Your request must be posted.')


form = cgi.FieldStorage()
required = ['username', 'password', 'dataset']
#username: Username
#password: Password
#dataset: Which data group to post to.
for param in required:
    if not param in required:
        die('missingparam', 'The parameter "{0}" was missing.'.format(param))

username = form['username'].value
if not username in access:
    die('notauthorized', 'Your username has not been authorized for access.')

if form['password'].value != access[username]['password']:
    die('wrongpass', 'Your password is wrong.')

if form['dataset'].value in access[username]['datasets']:
    die('notauthorized', 'Your account is not authorized for that dataset.')

#Yay, lets do it.

data = json.loads(form['data'].value)
r = requests.post(url, params=data)
print json.dumps(r.json())  # This seems silly.
