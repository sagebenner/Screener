from flask import Blueprint, render_template, session, request, redirect, url_for
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.utils
import numpy as np

research_views = Blueprint('research_views', __name__)

@research_views.route('/dashboard', methods=['post', 'get'])
def dashboard():

    return render_template('dashboard.html')

