from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_session import Session
import MySQLdb.cursors

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    process = []
    global session
    session = Session()
    session.init_app(app)

    mysql.init_app(app)
    
    from .screener_views import screener_views
    from .login import login
    app.register_blueprint(screener_views, url_prefix='/screener/')
    app.register_blueprint(login, url_prefix='/')

    return app

