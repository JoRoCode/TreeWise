from flask_app import app
from flask import render_template, redirect, request, session, Flask
from flask_app.models import tree, picture,quiz

# Create Quiz controller
@app.post('/process')
def get_quiz_results():
    data = request.form.get('score')
    print(session)
    print("DATA!!!", data)
    quiz_data = {'score' : data ,
            'user_id': session['user_id']}
    print("QDATA!!!", quiz_data)
    quiz.Quiz.submit_quiz_results(quiz_data)
    return 

# Read Quiz controller
@app.get('/quiz')
def see_quiz_page():
    return render_template('quiz.html')
# Update Quiz controller

# Delete Quiz controller