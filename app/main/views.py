from . import main
from flask import request, render_template
from flask_login import current_user

@main.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')
