# learning.py
from flask import Blueprint, render_template, redirect, url_for, request
from models import VocabularyItem, PhraseItem, db, GrammarLesson, UserProgress
from utils import get_current_user
from datetime import datetime
from translate import Translator


learning = Blueprint('learning', __name__)


@learning.route('/learning', methods=['GET', 'POST'])
def index():
    current_user = get_current_user()
    translation = None
    if request.method == 'POST':
       text = request.form.get('text')
       direction = request.form.get('direction')
       from_lang, to_lang = direction.split('-')
       translator = Translator(from_lang=from_lang, to_lang=to_lang)
       translation = translator.translate(text)
    return render_template('learning.html', current_user=get_current_user(), translation=translation)
    
    
    
    
    #return render_template('learning.html', current_user=current_user)




@learning.route('/learning/vocabulary/<int:lesson_number>', methods=['GET', 'POST'])
def vocabulary_lesson(lesson_number):
    if lesson_number not in [1, 2]:
        return redirect(url_for('learning.index'))
    
    user = get_current_user()  # Use get_current_user instead of current_user
    if user:  # Check if user is logged in
        progress = UserProgress.query.filter_by(
            user_id=user.id,
            content_type='vocabulary',
            lesson_number=lesson_number
        ).first()
        
        if not progress:
            mark_lesson_complete(user.id, 'vocabulary', lesson_number)

    translation = None
    if request.method == 'POST':
        text = request.form.get('text')
        direction = request.form.get('direction')
        from_lang, to_lang = direction.split('-')
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        translation = translator.translate(text)
    
    vocabulary_items = VocabularyItem.query.filter_by(lesson_number=lesson_number).all()
    return render_template('vocabulary_lesson.html',
                         items=vocabulary_items,
                         lesson_number=lesson_number,
                         translation=translation,
                         current_user=get_current_user())
    
    

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

        # Add all items to database
        for item in lesson1_items + lesson2_items:
            vocab_item = VocabularyItem(**item)
            db.session.add(vocab_item)

        db.session.commit()

        

@learning.route('/learning/phrases/<int:lesson_number>', methods=['GET', 'POST'])
def phrases_lesson(lesson_number):
    current_user = get_current_user()

    translation = None
    
    if request.method == 'POST':
        text = request.form.get('text')
        direction = request.form.get('direction')
        from_lang, to_lang = direction.split('-')
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        translation = translator.translate(text)

    if current_user:
        mark_lesson_complete(current_user.id, 'phrases', lesson_number)
    
    if lesson_number not in [1, 2]:
        return redirect(url_for('learning.index'))
    
    phrase_items = PhraseItem.query.filter_by(lesson_number=lesson_number).all()
    return render_template('phrases_lesson.html',
                         items=phrase_items,
                         lesson_number=lesson_number,
                         current_user=current_user,
                         translation=translation)

def init_phrases():
    if PhraseItem.query.first() is None:
        # Lesson 1: Basic Greetings and Common Phrases
        lesson1_items = [
            {
                'italian_phrase': 'Ciao!',
                'english_phrase': 'Hello!/Goodbye!',
                'pronunciation': 'chow',
                'lesson_number': 1,
                'category': 'greetings'
            },
            {
                'italian_phrase': 'Buongiorno!',
                'english_phrase': 'Good morning!',
                'pronunciation': 'bwohn-JHOR-noh',
                'lesson_number': 1,
                'category': 'greetings'
            },
            {
                'italian_phrase': 'Come stai?',
                'english_phrase': 'How are you?',
                'pronunciation': 'KOH-meh STY',
                'lesson_number': 1,
                'category': 'greetings'
            },
            {
                'italian_phrase': 'Per favore',
                'english_phrase': 'Please',
                'pronunciation': 'pehr fah-VOH-reh',
                'lesson_number': 1,
                'category': 'common_phrases'
            },
            {
                'italian_phrase': 'Grazie',
                'english_phrase': 'Thank you',
                'pronunciation': 'GRAH-tsee-eh',
                'lesson_number': 1,
                'category': 'common_phrases'
            }
        ]

        # Lesson 2: Phrases using vocabulary
        lesson2_items = [
            {
                'italian_phrase': 'Dov\'è la stazione?',
                'english_phrase': 'Where is the station?',
                'pronunciation': 'doh-VEH lah sta-tsee-OH-neh',
                'lesson_number': 2,
                'category': 'using_vocabulary'
            },
            {
                'italian_phrase': 'Mi piace la pasta',
                'english_phrase': 'I like pasta',
                'pronunciation': 'mee pee-AH-cheh lah PAH-stah',
                'lesson_number': 2,
                'category': 'using_vocabulary'
            },
            {
                'italian_phrase': 'Vado al parco',
                'english_phrase': 'I\'m going to the park',
                'pronunciation': 'VAH-doh ahl PAR-koh',
                'lesson_number': 2,
                'category': 'using_vocabulary'
            },
            {
                'italian_phrase': 'Il treno è in ritardo',
                'english_phrase': 'The train is late',
                'pronunciation': 'eel TREH-noh eh in ree-TAR-doh',
                'lesson_number': 2,
                'category': 'using_vocabulary'
            }
        ]

        # Add all items to database
        for item in lesson1_items + lesson2_items:
            phrase_item = PhraseItem(**item)
            db.session.add(phrase_item)


        db.session.commit()



@learning.route('/learning/grammar/<int:lesson_number>', methods=['GET', 'POST'])
def grammar_lesson(lesson_number):
    current_user = get_current_user()


    translation = None
    
    if request.method == 'POST':
        text = request.form.get('text')
        direction = request.form.get('direction')
        from_lang, to_lang = direction.split('-')
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        translation = translator.translate(text)

    if current_user:
        mark_lesson_complete(current_user.id, 'grammar', lesson_number)
    if lesson_number not in [1, 2]:
        return redirect(url_for('learning.index'))
    
    grammar_item = GrammarLesson.query.filter_by(lesson_number=lesson_number).first()
    return render_template('grammar_lesson.html',
                         lesson=grammar_item,
                         lesson_number=lesson_number,
                         current_user=current_user,
                         translation=translation)

def init_grammar():
    if GrammarLesson.query.first() is None:
        lessons = [
            {
                'title': 'Italian Genders and Grammar Overview',
                'content': '''
                <h3>Italian Genders</h3>
                <p>In Italian, every noun has a gender - either masculine or feminine. Unlike English, there is no neutral gender. Also pay attention to the articles used. In this case, "il" is masculine singular and "la" is feminine singular.</p>
                
                <h4>Masculine Nouns (-o)</h4>
                <ul>
                    <li>il libro (the book)</li>
                    <li>il tavolo (the table)</li>
                </ul>

                <h4>Feminine Nouns (-a)</h4>
                <ul>
                    <li>la casa (the house)</li>
                    <li>la sedia (the chair)</li>
                </ul>

                <h3>Basic Grammar Structure</h3>
                <p>Italian sentence structure is similar to English: Subject + Verb + Object</p>
                ''',
                'lesson_number': 1,
                'category': 'grammar_basics'
            },
            {
                'title': 'Italian Alphabet and Pronunciation',
                'content': '''
                <h3>The Italian Alphabet</h3>
                <p>The Italian alphabet has 21 letters (missing K, W, X, Y, J)</p>

                <h4>Key Differences from English</h4>
                <ul>
                    <li>C: "ch" before e/i, "k" before a/o/u</li>
                    <li>G: "j" before e/i, "g" before a/o/u</li>
                    <li>H: Always silent</li>
                    <li>R: Rolled/trilled</li>
                </ul>

                <h4>Vowels</h4>
                <p>A (ah), E (eh), I (ee), O (oh), U (oo)</p>
                ''',
                'lesson_number': 2,
                'category': 'pronunciation'
            }
        ]
        
        for lesson in lessons:
            grammar_item = GrammarLesson(**lesson)
            db.session.add(grammar_item)
        db.session.commit()

def mark_lesson_complete(user_id, content_type, lesson_number):
    progress = UserProgress.query.filter_by(
        user_id=user_id,
        content_type=content_type,
        lesson_number=lesson_number
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=user_id,
            content_type=content_type,
            lesson_number=lesson_number,
            completed=True
        )
        db.session.add(progress)
    else:
        progress.completed = True
        progress.completion_date = datetime.utcnow()
    
    db.session.commit()


