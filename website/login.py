from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import numpy as np
import plotly.utils
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.offline as pyo
import base64
from io import BytesIO
import json
from flask_mysqldb import MySQL

login = Blueprint('login', __name__)

@login.route('/', methods=['post', 'get'])
def start():
    if request.method=='POST':
        user_option = request.form.get('survey')
        session['user_option'] = user_option
        if user_option == 'clinical':
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login.research'))
    return render_template('start.html')

@login.route('/research', methods=['post', 'get'])
def research():
    if request.method=='POST':
        if request.form['result']=='back':
            return redirect(url_for('login.start'))
    return render_template('research.html')

@login.route('/register', methods=['post', 'get'])
def register():
    if request.method=='POST':
        if request.form['result']=='back':
            return redirect(url_for('login.start'))
    return render_template('register.html')

