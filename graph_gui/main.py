import argparse
import json
import os
import sys

from nocache import nocache
from flask import Flask, flash, jsonify, render_template, session
from flask import request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename

DATA_FOLDER = 'static/data/'
ALLOWED_EXT = set(['txt', 'json', 'csv', 'tsv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DATA_FOLDER
app.config['DATA_FOLDER'] = DATA_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/_upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('index'))
    
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            return jsonify(file.read())
    return redirect(url_for('index'))
    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route("/data/<filename>")
def data(filename):
    return send_from_directory(app.config['DATA_FOLDER'], filename)
    
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


def install_secret_key(app, filename='secret_key'):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.

    """
    filename = os.path.join(app.instance_path, filename)
    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print 'Error: No secret key. Create it with:'
        if not os.path.isdir(os.path.dirname(filename)):
            print 'mkdir -p', os.path.dirname(filename)
        print 'head -c 24 /dev/urandom >', filename
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Graph GUI Web Interface')
    parser.add_argument('--host', default='0.0.0.0', help='HTTP host')
    parser.add_argument('--port', type=int, default=5000, help='HTTP port')
    args = parser.parse_args()

    install_secret_key(app)
    app.run(args.host, args.port, debug=True)
