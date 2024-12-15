#app.py
from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, VocabularyItem, PhraseItem, GrammarLesson, PronunciationExercise, WritingExercise, ReadingExercise, UserProgress
import os
from routes.learning import learning, init_vocabulary, init_phrases, init_grammar
from routes.practicing import practicing
from utils import get_current_user

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

'''
# Learning section routes
@app.route('/learning')
def learning():
    current_user = get_current_user()
    return render_template('learning.html', current_user=current_user)
'''
'''
@app.route('/practicing')
def practicing():
    current_user = get_current_user()
    return render_template('practicing.html', current_user=current_user)
'''

@app.route('/extra-resources')
def extra_resources():
    current_user = get_current_user()
    return render_template('extra_resources.html', current_user=current_user)
    

# Information routes
@app.route('/about')
def about():
    current_user = get_current_user()
    return render_template('about.html', current_user=current_user)

@app.route('/contact')
def contact():
    current_user = get_current_user()
    return render_template('contact.html', current_user=current_user)


# User routes
@app.route('/user')
def user():
    current_user = get_current_user()
    return render_template('user.html', current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
            
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('signup'))
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/progress')
def user_progress():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))
        
    # Get progress for each type of content
    vocabulary_progress = {
        progress.lesson_number: progress.completed 
        for progress in UserProgress.query.filter_by(
            user_id=current_user.id, 
            content_type='vocabulary'
        ).all()
    }
    
    phrases_progress = {
        progress.lesson_number: progress.completed 
        for progress in UserProgress.query.filter_by(
            user_id=current_user.id, 
            content_type='phrases'
        ).all()
    }
    
    grammar_progress = {
        progress.lesson_number: progress.completed 
        for progress in UserProgress.query.filter_by(
            user_id=current_user.id, 
            content_type='grammar'
        ).all()
    }

    pronunciation_progress = {
        progress.lesson_number: progress.completed 
        for progress in UserProgress.query.filter_by(
            user_id=current_user.id, 
            content_type='pronunciation_practice'
        ).all()
    }
    
    writing_progress = {
        progress.lesson_number: progress.completed 
        for progress in UserProgress.query.filter_by(
            user_id=current_user.id, 
            content_type='writing_practice'
        ).all()
    }
    
    reading_progress = {
        progress.lesson_number: progress.completed 
        for progress in UserProgress.query.filter_by(
            user_id=current_user.id, 
            content_type='reading_practice'
        ).all()
    }
    
    return render_template('user_progress.html',
                         # learning progress
                         vocabulary_progress=vocabulary_progress,
                         phrases_progress=phrases_progress,
                         grammar_progress=grammar_progress,
                         # practice progress
                         pronunciation_progress=pronunciation_progress,
                         writing_progress=writing_progress,
                         reading_progress=reading_progress,
                         current_user=current_user)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This creates the database tables
        init_vocabulary()
        init_phrases()
        init_grammar()
    app.run(debug=True)
