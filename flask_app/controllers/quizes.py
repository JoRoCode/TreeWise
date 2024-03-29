from flask_app import app
from flask import render_template, redirect, request, session, Flask
from flask_app.models import tree, picture,quiz

# Create Quiz controller
@app.post('/process')
def get_quiz_results():
    if 'user_id' not in session: return redirect('/')
    data = request.form.get('score')
    quiz_data = {'score' : data ,
        'user_id': session['user_id']}
    quiz.Quiz.submit_quiz_results(quiz_data)
    return 

# Read Quiz controller
@app.get('/quiz')
def see_quiz_page():
    if 'user_id' not in session: return redirect('/')
    return render_template('quiz.html')
# Update Quiz controller

# Delete Quiz controller