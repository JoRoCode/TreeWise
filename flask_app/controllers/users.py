from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, quiz # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Users Controller

@app.post('/user/register')
def create_new_user():
    if user.User.create_new_user(request.form):
        return redirect('/home') # redirect to the show page
    return redirect('/register')

# Read Users Controller

@app.get('/')
def index():
    return render_template('index.html')


@app.get('/register')
def register():
    return render_template('register.html')

@app.get('/login')
def login():
    return render_template('login.html')


@app.get('/importance')
def importance():
    if 'user_id' not in session: return redirect('/')
    return render_template('importance.html')



@app.get('/user/account')
def show_user_account():
    if 'user_id' not in session: return redirect('/')
    user_data = user.User.get_user_by_id(session['user_id'])
    quiz_data = quiz.Quiz.get_all_quizs_by_user_id(session['user_id'])
    return render_template('account.html', user = user_data, quiz_data = quiz_data)

# Update Users Controller
@app.post('/user/update')
def update_user_account():
    if 'user_id' not in session: return redirect('/')
    user.User.update_user_info(request.form)
    return redirect('/user/account')


# Delete Users Controller
@app.post('/user/account/delete')
def delete_user_account():
    if 'user_id' not in session: return redirect('/')
    user.User.delete_user_account(session['user_id'])
    session.clear()
    return redirect('/')


# login user

@app.post('/user/login')
def log_user_in():
    if user.User.log_user_in(request.form):
        return redirect('/home')
    return redirect('/login')


# log user out

@app.route('/user/logout')
def log_user_out():
    session.clear()
    return redirect('/')