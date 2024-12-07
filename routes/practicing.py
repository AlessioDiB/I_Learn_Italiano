from flask import Blueprint, render_template

practicing = Blueprint('practicing', __name__)

@practicing.route('/practising')
def index():
    return render_template('practising.html')