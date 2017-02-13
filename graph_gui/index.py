import argparse
import os

from flask import Flask, flash, jsonify, render_template 
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
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/data/<filename>")
def data(filename):
    return send_from_directory(app.config['DATA_FOLDER'], filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Graph GUI Web Interface')
    parser.add_argument('--host', default='0.0.0.0', help='HTTP host')
    parser.add_argument('--port', type=int, default=5000, help='HTTP port')
    args = parser.parse_args()

    app.run(args.host, args.port, debug=True)
