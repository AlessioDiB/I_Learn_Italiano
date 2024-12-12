from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, VocabularyItem
import os
from routes.learning import learning, init_vocabulary  # Import both blueprint and function
from routes.practicing import practicing

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Register blueprints
app.register_blueprint(learning)
app.register_blueprint(practicing)

# User authentication helper
def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

with app.app_context():
    db.create_all()  # Creates the tables
    init_vocabulary()  # Initialize vocabulary items

    
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

'''
@app.route('/check_image')
def check_image():
    import os
    image_path = os.path.join(os.getcwd(), 'static', 'images', 'homepage_web_draft_1.png')
    exists = os.path.exists(image_path)
    return f"""
    <h1>Image Check</h1>
    <p>Image path: {image_path}</p>
    <p>File exists: {exists}</p>
    <img src="/static/images/homepage_web_draft_1.png" alt="test">
    """


@app.route('/learning')
def learning():
    return render_template('learning.html')


@app.route('/learning/vocabulary/<int:lesson_number>')
def vocabulary_lesson(lesson_number):
    if lesson_number not in [1, 2]:
        return redirect(url_for('learning'))
        
    vocabulary_items = VocabularyItem.query.filter_by(lesson_number=lesson_number).all()
    return render_template('vocabulary_lesson.html', 
                         items=vocabulary_items, 
                         lesson_number=lesson_number)

'''

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This creates the database tables
    app.run(debug=True)