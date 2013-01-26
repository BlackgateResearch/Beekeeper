# I dedicate any and all copyright interest in this software to the
# public domain. I make this dedication for the benefit of the public at
# large and to the detriment of my heirs and successors. I intend this
# dedication to be an overt act of relinquishment in perpetuity of all
# present and future rights to this software under copyright law.
# unlicense.org

import os

from flask import Flask
from furl import furl

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello():

    args = {
        'client_id': '981b4763b9ba42e888777a0c8d03e02b',
        'response_type': 'code',
        'redirect_uri': 'http://beekeeper.herokuapp.com/'
    }

    url = furl('https://runkeeper.com/apps/authorize').add(args).url
    return '<a href=%s>Authorise</a>' % url


@app.route('/test/<value>')
def show_user_profile(value):
    # show the user profile for that user
    return 'got %s' % value

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
