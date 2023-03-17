from flask import Blueprint, render_template

screener_views = Blueprint('screener_views', __name__)

@screener_views.route('/home', methods=['post', 'get'])
def home():
    return render_template('home.html')


