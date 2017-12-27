# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask, request, url_for, send_from_directory
from werkzeug import secure_filename
import cv2
import face
import time

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['HAT_FILE'] = os.path.join(app.config['UPLOAD_FOLDER'], 'Santa-hat-icon.png') 
app.config['MAX_CONTENT_LENGTH'] = 16 * 4096 * 4096


html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>Photo Upload</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=upload>
    </form>
    '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            hat_file = app.config['HAT_FILE']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            face_img = face.santa(upload_file, hat_file)
            save_img = "{}_{}".format(int(time.time()), filename)
            cv2.imwrite(save_img, face_img)
            file_url = url_for('uploaded_file', filename=save_img)
            return html + '<br><img src=' + file_url + '>'
        else:
            print >> sys.stderr, "img: %s format invalid" % file.filename
    return html


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9998)
