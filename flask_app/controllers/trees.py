from flask_app import app
from flask import render_template, redirect, request, session, Flask
from flask_app.models import tree, picture
from werkzeug.utils import secure_filename


# Create Tree Controller

@app.post('/create/tree')
def create_new_tree():
    if 'user_id' not in session: return redirect('/')
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
    if 'user_id' not in session: return redirect('/')
    tree.Tree.delete_tree(request.form)
    return redirect('/admin')

# Search controller

@app.post('/species/search')
def search_by_common_name():
    if 'user_id' not in session: return redirect('/')
    tree_name = request.form['name']
    tree_data = tree.Tree.get_tree_by_multiple_varieables(tree_name)
    if tree_data:
        return redirect(f'/species/{tree_data}')
    return redirect('/species')
