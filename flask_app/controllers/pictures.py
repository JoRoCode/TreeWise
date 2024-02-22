import os
from flask_app import app
from flask import  redirect, request, Flask, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_app.models import picture

app.config['UPLOAD_FOLDER'] = 'flask_app/static/images/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'.png', '.jpg', '.jpeg', '.gif'}


@app.post('/upload/picture')
def upload_file():
    if session['user_id'] != 1: return redirect('/home')
    file = request.files['picture']
    extension = os.path.splitext(file.filename)[1]
    if 'picture' not in request.files:
        flash('No file part')
        return redirect('/admin')
    if file.filename == '':
        flash('No file selected')
        return redirect('/admin')
    if file:
        print(file, "!!!!!!!!!!!!!!!!1")
        if extension not in app.config['ALLOWED_EXTENSIONS']:
            flash('File is not an image')
            return redirect('/admin')
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'],
            secure_filename(file.filename)))
        flash('Image successfully uploaded.')
        print(file)
        print(secure_filename(file.filename))
    picture.Picture.add_picture_to_database(
        secure_filename(file.filename), 
        request.form['id'])
    return redirect('/admin')

@app.get('/serve_image/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
