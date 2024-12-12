# vocabulary_lesson.html
from flask import Blueprint, render_template, redirect, url_for
from models import VocabularyItem, db

learning = Blueprint('learning', __name__)

@learning.route('/learning')
def index():
    return render_template('learning.html')

@learning.route('/learning/vocabulary/<int:lesson_number>')
def vocabulary_lesson(lesson_number):
    if lesson_number not in [1, 2]:
        return redirect(url_for('learning.index'))
        
    vocabulary_items = VocabularyItem.query.filter_by(lesson_number=lesson_number).all()
    print(f"Found {len(vocabulary_items)} items for lesson {lesson_number}")  # Debug print
    return render_template('vocabulary_lesson.html',
                         items=vocabulary_items,
                         lesson_number=lesson_number)

def init_vocabulary():
    # Check if we already have vocabulary items
    if VocabularyItem.query.first() is None:
        # Lesson 1: House items and Food
        lesson1_items = [
            {
                'italian_word': 'la tavola',
                'english_word': 'table',
                'image_url': '/static/images/vocabulary/table.jpg',
                'lesson_number': 1,
                'category': 'house'
            },
            {
                'italian_word': 'la sedia',
                'english_word': 'chair',
                'image_url': '/static/images/vocabulary/chair.jpg',
                'lesson_number': 1,
                'category': 'house'
            },
            {
                'italian_word': 'il letto',
                'english_word': 'bed',
                'image_url': '/static/images/vocabulary/bed.jpg',
                'lesson_number': 1,
                'category': 'house'
            },
            {
                'italian_word': 'la pizza',
                'english_word': 'pizza',
                'image_url': '/static/images/vocabulary/pizza.jpg',
                'lesson_number': 1,
                'category': 'food'
            },
            {
                'italian_word': 'la pasta',
                'english_word': 'pasta',
                'image_url': '/static/images/vocabulary/pasta.jpg',
                'lesson_number': 1,
                'category': 'food'
            }
        ]

        # Lesson 2: Places and Transportation
        lesson2_items = [
            {
                'italian_word': 'la stazione',
                'english_word': 'station',
                'image_url': '/static/images/vocabulary/station.jpg',
                'lesson_number': 2,
                'category': 'places'
            },
            {
                'italian_word': 'il treno',
                'english_word': 'train',
                'image_url': '/static/images/vocabulary/train.jpg',
                'lesson_number': 2,
                'category': 'transport'
            },
            {
                'italian_word': 'l\'autobus',
                'english_word': 'bus',
                'image_url': '/static/images/vocabulary/bus.jpg',
                'lesson_number': 2,
                'category': 'transport'
            },
            {
                'italian_word': 'il parco',
                'english_word': 'park',
                'image_url': '/static/images/vocabulary/park.jpg',
                'lesson_number': 2,
                'category': 'places'
            },
            {
                'italian_word': 'la biblioteca',
                'english_word': 'library',
                'image_url': '/static/images/vocabulary/library.jpg',
                'lesson_number': 2,
                'category': 'places'
            }
        ]

    try:
            # Check if we already have vocabulary items
            if VocabularyItem.query.first() is None:
                print("Initializing vocabulary items...")
                # Add all items to database
                for item in lesson1_items + lesson2_items:
                    vocab_item = VocabularyItem(**item)
                    db.session.add(vocab_item)
                db.session.commit()
                print("Vocabulary items initialized successfully")
            else:
                print("Vocabulary items already exist in database")
    except Exception as e:
            print(f"Error initializing vocabulary: {e}")
            db.session.rollback()








            '''
            # Add all items to database
            for item in lesson1_items + lesson2_items:
                vocab_item = VocabularyItem(**item)
                db.session.add(vocab_item)
            
            
            db.session.commit()
            '''