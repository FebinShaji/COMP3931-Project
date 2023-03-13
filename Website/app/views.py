from flask import render_template
from app import app
from .forms import *
from .models import *

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
