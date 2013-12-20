from flask import Flask, render_template, send_from_directory, redirect, url_for, request
from werkzeug import secure_filename

import qrcode

import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads' + os.sep
app.config['STATIC_FOLDER'] = 'static' + os.sep
app.config['HOST'] = 'http://bc-gen.yu-lu.info'


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/upload", methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        sf = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + sf)
        img = qrcode.make(app.config['HOST'] + '/uploads/' + sf)
        img.save(app.config['STATIC_FOLDER'] + sf + '.png')
        return redirect(url_for('barcode', filename=sf))
    else:
        return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename);

@app.route('/barcode/<filename>')
def barcode(filename):
    url = app.config['HOST'] + '/static/' + filename + '.png'
    file_url = app.config['HOST'] + '/uploads/' + filename
    return render_template('barcode.html', filename=filename, file_url=file_url, url=url)

if __name__ == '__main__':
    app.debug = True
    app.run()
