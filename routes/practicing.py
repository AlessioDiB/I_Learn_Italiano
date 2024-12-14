# practicing.py
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from models import PronunciationExercise, WritingExercise, ReadingExercise, db
from gtts import gTTS
import os

practicing = Blueprint('practicing', __name__)

@practicing.route('/practicing')
def index():
    return render_template('practicing.html')



@practicing.route('/practicing/writing/<int:lesson_number>')
def writing_lesson(lesson_number):
    exercise = WritingExercise.query.filter_by(lesson_number=lesson_number).first()
    return render_template('writing_practice.html',
                         exercise=exercise,
                         lesson_number=lesson_number)

@practicing.route('/save_writing_response', methods=['POST'])
def save_writing_response():
    response = request.form.get('response')
    exercise_id = request.form.get('exercise_id')
    
    # Here you can add code to handle the response
    # For example, save it to database, check it, etc.
    
    # For now, let's just redirect back to the writing lesson
    return redirect(url_for('practicing.writing_lesson', lesson_number=1))


@practicing.route('/practicing/reading/<int:lesson_number>')
def reading_lesson(lesson_number):
    # Example questions for Lesson 1
    if lesson_number == 1:
        exercise = {
            'text': "La Casa di Maria\n\nMaria è a casa. La casa ha una tavola e quattro sedie. Sulla tavola c'è una pizza. La pizza è buona! Maria mangia la pasta anche. Nel suo letto, Maria legge un libro.",
            'questions': [
                {
                    'question': 'Dove è Maria?',
                    'options': ['A casa', 'Al parco', 'In biblioteca', 'Alla stazione'],
                    'correct_answer': 0
                },
                {
                    'question': "Cosa c'è sulla tavola?",
                    'options': ['Una pasta', 'Una pizza', 'Un libro', 'Una sedia'],
                    'correct_answer': 1
                },
                {
                    'question': 'Cosa fa Maria nel letto?',
                    'options': ['Dorme', 'Mangia', 'Legge', 'Studia'],
                    'correct_answer': 2
                }
            ]
        }
    # Example questions for Lesson 2
    else:
        exercise = {
            'text': "Una Giornata in Città\n\nMaria va alla stazione in autobus. Dalla stazione, prende il treno per andare in città. In città, Maria cammina al parco. Dopo il parco, va alla biblioteca per studiare. La biblioteca è grande e bella! Maria legge molti libri qui. Quando ha fame, mangia una pizza al tavolo di un ristorante vicino alla biblioteca.",
            'questions': [
                {
                    'question': 'Come va Maria alla stazione?',
                    'options': ['In treno', 'In autobus', 'A piedi', 'In bicicletta'],
                    'correct_answer': 1
                },
                {
                    'question': 'Dove va Maria dopo il parco?',
                    'options': ['Al ristorante', 'Alla stazione', 'Alla biblioteca', 'A casa'],
                    'correct_answer': 2
                },
                {
                    'question': 'Cosa fa Maria quando ha fame?',
                    'options': ['Va a casa', 'Mangia una pizza', 'Va in biblioteca', 'Prende il treno'],
                    'correct_answer': 1
                }
            ]
        }
    return render_template('reading_practice.html', exercise=exercise, lesson_number=lesson_number)

@practicing.route('/practicing/check_answers/<int:lesson_number>', methods=['POST'])
def check_answers(lesson_number):
    # Get the exercise data again (you might want to store this in a session)
    if lesson_number == 1:
        correct_answers = [0, 1, 2]  # Correct answers for lesson 1
    else:
        correct_answers = [1, 2, 1]  # Correct answers for lesson 2

    score = 0
    for i in range(3):  # We have 3 questions
        user_answer = request.form.get(f'question{i + 1}')
        if user_answer and int(user_answer) == correct_answers[i]:
            score += 1
    
    flash(f'You scored {score} out of 3!')
    return redirect(url_for('practicing.reading_lesson', lesson_number=lesson_number))



@practicing.route('/practicing/pronunciation/<int:lesson_number>')
def pronunciation_lesson(lesson_number):
    if lesson_number == 1:
        exercises = {
            'title': 'Basic Sounds',
            'words': [
                {'italian': 'casa', 'english': 'house', 'phonetic': 'kah-sah'},
                {'italian': 'tavola', 'english': 'table', 'phonetic': 'tah-voh-lah'},
                {'italian': 'sedia', 'english': 'chair', 'phonetic': 'seh-dee-ah'},
                {'italian': 'pizza', 'english': 'pizza', 'phonetic': 'peet-sah'},
                {'italian': 'pasta', 'english': 'pasta', 'phonetic': 'pah-stah'}
            ]
        }
    else:
        exercises = {
            'title': 'Complex Sounds',
            'words': [
                {'italian': 'biblioteca', 'english': 'library', 'phonetic': 'bee-blee-oh-teh-kah'},
                {'italian': 'stazione', 'english': 'station', 'phonetic': 'stah-tzee-oh-neh'},
                {'italian': "l'autobus", 'english': 'bus', 'phonetic': 'lau-toh-boos'},
                {'italian': 'quando', 'english': 'when', 'phonetic': 'kwan-doh'},
                {'italian': 'anche', 'english': 'also', 'phonetic': 'ahn-keh'}
            ]
        }
    
    return render_template('pronunciation_practice.html',
                         exercises=exercises,
                         lesson_number=lesson_number)

@practicing.route('/practicing/generate_audio/<word>')
def generate_audio(word):
    tts = gTTS(text=word, lang='it')
    audio_path = f"static/audio/{word}.mp3"
    os.makedirs('static/audio', exist_ok=True)
    tts.save(audio_path)
    return jsonify({'audio_url': '/' + audio_path})