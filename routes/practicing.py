# practicing.py
from flask import Blueprint, render_template
from models import PronunciationExercise, WritingExercise, ReadingExercise, db

practicing = Blueprint('practicing', __name__)

@practicing.route('/practicing')
def index():
    return render_template('practicing.html')

@practicing.route('/practicing/pronunciation/<int:lesson_number>')
def pronunciation_lesson(lesson_number):
    exercises = PronunciationExercise.query.filter_by(lesson_number=lesson_number).all()
    return render_template('pronunciation_practice.html',
                         exercises=exercises,
                         lesson_number=lesson_number)

@practicing.route('/practicing/writing/<int:lesson_number>')
def writing_lesson(lesson_number):
    exercise = WritingExercise.query.filter_by(lesson_number=lesson_number).first()
    return render_template('writing_practice.html',
                         exercise=exercise,
                         lesson_number=lesson_number)

@practicing.route('/practicing/reading/<int:lesson_number>')
def reading_lesson(lesson_number):
    exercise = ReadingExercise.query.filter_by(lesson_number=lesson_number).first()
    return render_template('reading_practice.html',
                         exercise=exercise,
                         lesson_number=lesson_number)