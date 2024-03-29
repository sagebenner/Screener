from flask import Flask, render_template, request, redirect, url_for, session, flash

from flask_session import Session




def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    process = []
    global session
    session = Session()
    session.init_app(app)
    
    from .screener_views import screener_views
    from .login import login
    from .research_views import research_views
    from .short_form import short_form
    app.register_blueprint(login, url_prefix='/registration')
    app.register_blueprint(screener_views, url_prefix='/')
    app.register_blueprint(research_views, url_prefix='/research/')
    app.register_blueprint(short_form, url_prefix='/short_form/')

    return app

