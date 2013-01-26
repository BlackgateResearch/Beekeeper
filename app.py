# I dedicate any and all copyright interest in this software to the
# public domain. I make this dedication for the benefit of the public at
# large and to the detriment of my heirs and successors. I intend this
# dedication to be an overt act of relinquishment in perpetuity of all
# present and future rights to this software under copyright law.
# unlicense.org

import os
import json

from flask import Flask, request, session, url_for, redirect
from furl import furl
import requests
from healthgraph import RunKeeperClient

app = Flask(__name__)
app.secret_key = '1A0Zr92138j/3asdfyX R~XHH!jsdfmN]LWX/,?RT~#'
app.debug = True
runkeeper_redirect_uri = 'http://beekeeper.herokuapp.com/new_goal/'
beeminder_redirect_uri = 'http://beekeeper.herokuapp.com/'


@app.route('/')
def index():
    at = request.args.get('access_token', False)
    if at:
        session['beeminder_access_token'] = at

    if session.get('beeminder_access_token', False):
        return """
        Welcome
        Here are you existing linked Goals:
        ...
        <a href=%s>Create new linked Goal</a>
        """ % url_for('new_goal')
    else:
        args = {
            'client_id': 'caekchatjlsjewirvmeymxzjm',
            'response_type': 'token',
            'redirect_uri': beeminder_redirect_uri
        }

        url = furl('https://www.beeminder.com/apps/authorize').add(args).url
        return '<a href=%s>Authorise Beeminder</a>' % url


@app.route('/new_goal/')
def new_goal():
    if request.args.get('code', False):
        payload = {
            'grant_type': 'authorization_code',
            'code': request.args['code'],
            'client_id': '981b4763b9ba42e888777a0c8d03e02b',
            'client_secret': 'af6d9f6a6c684139b5a86fd6ee64ac31',
            'redirect_uri': runkeeper_redirect_uri
        }
        r = requests.post("https://runkeeper.com/apps/token", data=payload)
        session['runkeeper_access_token'] = json.loads(r.text)['access_token']

    if session.get('runkeeper_access_token', False):
        client = RunKeeperClient(session['runkeeper_access_token'])
        return """
        Welcome
        Here are you existing weights:
        %s
        """ % client.getWeightMeasurements()
    else:
        args = {
            'client_id': '981b4763b9ba42e888777a0c8d03e02b',
            'response_type': 'code',
            'redirect_uri': runkeeper_redirect_uri
        }

        url = furl('https://runkeeper.com/apps/authorize').add(args).url
        return '<a href=%s>Authorise</a>' % url


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
