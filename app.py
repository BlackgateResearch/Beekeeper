import os
from flask import Flask

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello():
    return 'OK'


@app.route('/test/<value>')
def show_user_profile(value):
    # show the user profile for that user
    return 'got %s' % value

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
