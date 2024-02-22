from flask_app import app
from flask import render_template, redirect, request, session, Flask
from flask_app.models import tree, picture

# Create Quiz controller

# Read Quiz controller
@app.get('/quiz')
def see_quiz_page():
    return render_template('quiz.html')
# Update Quiz controller

# Delete Quiz controller