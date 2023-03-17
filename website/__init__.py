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
# from wtforms.validators import InputRequired
from flask_mysqldb import MySQL

import MySQLdb.cursors
import re
from os import path

def create_app():
    app = Flask(__name__)
    process = []

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'dsq_screener'
    mysql = MySQL(app)
    mysql.init_app(app)
    
    from .screener_views import screener_views
    from .login import login
    app.register_blueprint(screener_views, url_prefix='/')
    app.register_blueprint(login, url_prefix='/')

    return app

