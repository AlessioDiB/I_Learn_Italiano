from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)



@app.route('/learning')
def learning():
    return render_template('learning.html')

@app.route('/extra-resources')
def extra_resources():
    return render_template('extra_resources.html')

@app.route('/practising')
def practising():
    return render_template('practising.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/user')
def user():
    return render_template('user.html')


































'''
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)



-------------------------------------------------------------------



older 
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# .\.venv\Scripts\Activate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # sqlite easier to use # 4 / absolute path, 3 / relative path to reside in the project
db = SQLAlchemy(app) # initialise database with settings from app

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id column, integer that references the id of each entry
    content = db.Column(db.String(200), nullable=False)  # what holds each task
    # nullable = false. we don't want the user to create a new task and leave the content empty
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    # function to return a string every time a new element is created
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] # it's going to create a new task from that input
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task) # trying to commit to a database
            db.session.commit()
            return redirect('/')  #redirect back to our index
        except:
            return 'There was an issue adding your task'


    else:
        task = Todo.query.order_by(Todo.date_created).all() # look at the database content by the order they were created, and return them
        return render_template('index.html', task = task )    #task, to pass that to our template

@app.route('/delete/<int:id')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/') # return a redirect back to our homepage
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content'] # this current task content = the content in the form, in the box

        try:
            db.session.commit()
            return redirect('/') # redirect to homepage
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task = task)

if __name__ == "__main__":
    app.run(debug=True)

'''