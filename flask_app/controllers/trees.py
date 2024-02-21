from flask_app import app
from flask import render_template, redirect, request, session, Flask, flash, url_for
from flask_app.models import tree, picture
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# Create Tree Controller

@app.post('/create/tree')
def create_new_tree():
    tree.Tree.create_new_tree(request.form)
    return redirect('/admin')


# Read Tree Controller

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session['user_id'] != 1: return redirect('/home')
    trees = tree.Tree.get_all_trees()
    tree_data = tree.Tree.get_tree_by_id(request.form)
    return render_template('admin.html', trees=trees, tree=tree_data)

@app.get('/species')
def species():
    if 'user_id' not in session: return redirect('/')
    tree_data = tree.Tree.get_all_trees()
    return render_template('species.html', trees=tree_data)


@app.get("/species/<common_name>")
def show_tree(common_name):
    if 'user_id' not in session: return redirect('/')
    tree_data = tree.Tree.get_tree_by_common_name(common_name)
    pictures = picture.Picture.get_pictures_by_tree_common_name(common_name)
    return render_template('show_tree.html', tree=tree_data, pictures = pictures)

# Update Tree Controller

@app.post('/update/tree')
def update_one_tree():
    if session['user_id'] != 1: return redirect('/home')
    tree.Tree.update_this_tree(request.form)
    return redirect('/admin')

# Delete Tree Controller
@app.post('/tree/delete')
def delete_tree():
    tree.Tree.delete_tree(request.form)
    return redirect('/admin')

# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')                                   The variable must be in the path within angle brackets
# def index(id):                                            It must also be passed into the function as an argument/parameter
#     user_info = user.User.get_user_by_id(id)              The it will be able to be used within the function for that route
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.

# Render template is a function that takes in a template name in the form of a string, then any number of named arguments containing data to pass to that template where it will be integrated via the use of jinja
# Redirect redirects from one route to another, this should always be done following a form submission. Don't render on a form submission.