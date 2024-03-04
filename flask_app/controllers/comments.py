from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, comment

# Create Comment Controller

@app.post('/user/comment')
def create_new_comment():
    if comment.Comment.create_new_comment(request.form):
        return redirect('/home') # redirect to the show page
    return redirect('/home')

# Read Comment Controller

@app.get('/home')
def display_home_page():
    print(session, "This is session") 
    if 'user_id' not in session: return redirect('/')
    user_data = user.User.get_user_by_id(session['user_id'])
    comments = comment.Comment.get_all_comments_with_creator()
    return render_template('home.html', user = user_data, comments = comments )

# Delete Comments Controller

@app.get('/user/comment/delete/<int:comment_id>')
def delete_comment(comment_id):
    if 'user_id' not in session: return redirect('/')
    comment.Comment.delete_user_comment(comment_id)
    return redirect('/home')

# Update Comments Controller

@app.post('/user/comment/update')
def update_comment():
    if 'user_id' not in session: return redirect('/')
    comment.Comment.update_user_comment(request.form)
    return redirect('/home')
