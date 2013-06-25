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

import os
import requests
import simplejson as json
import yaml

from flask import Flask, request
app = Flask(__name__)
app.debug = True




url = 'http://stats.wmflabs.org:83/thing'


def die(code, message):
    return json.dumps({'error': {'code': code, 'message': message}})

with open(os.path.expanduser('~/access.yml'), 'r') as f:
    access = yaml.load(f)

@app.route('/v1/api/', methods=['POST'])
def forward_req():
    required = ['username', 'password', 'dataset']
    #username: Username
    #password: Password
    #dataset: Which data group to post to.
    for param in required:
        if not param in request:
            return die('missingparam', 'The parameter "{0}" was missing.'.format(param))

    username = request.form['username']
    if not username in access:
        return die('notauthorized', 'Your username has not been authorized for access.')

    if request.form['password'] != access[username]['password']:
        return die('wrongpass', 'Your password is wrong.')

    if request.form['dataset'] in access[username]['datasets']:
        return die('notauthorized', 'Your account is not authorized for that dataset.')

    #Yay, lets do it.

    data = json.loads(request.form['data'])
    r = requests.post(url, params=data)
    return json.dumps(r.json())  # This seems silly.
