#models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    progress = db.relationship('UserProgress', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class VocabularyItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    italian_word = db.Column(db.String(100), nullable=False)
    english_word = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    lesson_number = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Vocabulary {self.italian_word}>'
    


class PhraseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    italian_phrase = db.Column(db.String(200), nullable=False)
    english_phrase = db.Column(db.String(200), nullable=False)
    pronunciation = db.Column(db.String(200))  # Optional pronunciation guide
    lesson_number = db.Column(db.Integer, nullable=False)  # 1 or 2
    category = db.Column(db.String(50))  # greetings, common_phrases, etc.


class GrammarLesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    lesson_number = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))

class PronunciationExercise(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   word = db.Column(db.String(100), nullable=False)
   pronunciation_guide = db.Column(db.String(200), nullable=False)
   lesson_number = db.Column(db.Integer, nullable=False)

class WritingExercise(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   prompt = db.Column(db.String(200), nullable=False)
   example_answer = db.Column(db.Text, nullable=False)
   lesson_number = db.Column(db.Integer, nullable=False)

class ReadingExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    questions = db.Column(db.JSON, nullable=False)  # Store questions and answers as JSON
    lesson_number = db.Column(db.Integer, nullable=False)

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_type = db.Column(db.String(50))  # 'vocabulary', 'phrases', 'grammar'
    lesson_number = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime, default=datetime.utcnow)