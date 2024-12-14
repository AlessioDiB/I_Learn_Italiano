#app.py
from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, VocabularyItem, PhraseItem, GrammarLesson, PronunciationExercise, WritingExercise, ReadingExercise
import os
from routes.learning import learning, init_vocabulary, init_phrases, init_grammar
from routes.practicing import practicing

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'
db.init_app(app)

# Register blueprints
app.register_blueprint(learning)
app.register_blueprint(practicing)

# User authentication helper
def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


# Main routes
@app.route('/')
def index():
    current_user = get_current_user()
    return render_template('index.html', current_user=current_user)

# Learning section routes
@app.route('/learning')
def learning():
    return render_template('learning.html')

@app.route('/practising')
def practising():
    return render_template('practising.html')

@app.route('/extra-resources')
def extra_resources():
    return render_template('extra_resources.html')

# Information routes
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# User routes
@app.route('/user')
def user():
    return render_template('user.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This creates the database tables
        init_vocabulary()
        init_phrases()
        init_grammar()
    app.run(debug=True)
