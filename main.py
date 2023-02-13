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
#from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import probabilities

import MySQLdb.cursors
import re
from os import path


app = Flask(__name__)
process = []
app.config['SECRET_KEY'] = 'development'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'dsq'

#db = SQLAlchemy()
mysql = MySQL(app)




'''''
class DSQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fatigue = db.Column(db.Integer)
    minex = db.Column(db.Integer)
    unrefreshed = db.Column(db.Integer)
    remember = db.Column(db.Integer)

if not path.exists('Screener/' + DB_NAME):
    with app.app_context():
        db.create_all()


'''''



symptom = ["Fatigue", "Minimum exercise", "Sleep", "Remember"]
pagelist = ["example.html", "example2.html", "example3.html", "example4.html"]
pagenum = 0
end = False
pemdomain = 0
sleepdomain = 0
cogdomain = 0
survey = str
message = "*Please enter a response for both frequency and severity before continuing"

def diagnose():
    global end
    df = pd.read_csv('MECFS VS OTHERS BINARY.csv')

    fatiguescore = (int(session["fatiguescoref"]) + int(session["fatiguescores"])) / 2

    if survey == "rf4":
        import probabilities
        pemscore = (int(session["minexf"]) + int(session["minexf"])) / 2
        sleepscore = (int(session["sleepf"]) + int(session["sleeps"])) / 2
        cogscore = (int(session["rememberf"]) + int(session["remembers"])) / 2
        data = np.array([[fatiguescore, pemscore, sleepscore, cogscore]])

    if survey == "rf14":
        import randomForest
        import probabilities
        pemscore = (int(session["minexf"]) + int(session["minexs"])) / 2
        sleepscore = (int(session["sleepf"]) + int(session["sleeps"])) / 2
        cogscore = (int(session["rememberf"]) + int(session["remembers"])) / 2
        df = pd.read_csv('MECFS VS OTHERS BINARY.csv')
        data = [fatiguescore, ((int(session["soref"]) + int(session["sores"])) / 2), pemscore,
                          ((int(session["sleepf"]) + int(session["sleeps"])) / 2),
                          ((int(session["musclef"]) + int(session["muscles"])) / 2),
                          ((int(session["bloatf"]) + int(session["bloats"])) / 2), cogscore,
                          ((int(session["attentionf"]) + int(session["attentions"])) / 2),
                          ((int(session["bowelf"]) + int(session["bowels"])) / 2),
                          ((int(session["unsteadyf"]) + int(session["unsteadys"])) / 2),
                          ((int(session["limbsf"]) + int(session["limbss"])) / 2),
                          ((int(session["hotf"]) + int(session["hots"])) / 2),
                          ((int(session["fluf"]) + int(session["flus"])) / 2),
                          ((int(session["smellf"]) + int(session["smells"])) / 2)]

        newdf = df[(df['fatigue13c'] >= (data[0] - 1)) &
                   (df['fatigue13c'] <= (data[0] + 1)) &
                   (df['soreness15c'] >= (data[1] - 1)) &
                   (df['soreness15c'] <= (data[1] + 1)) &
                   (df['minimum17c'] >= (data[2] - 1)) &
                   (df['minimum17c'] <= (data[2] + 1)) &
                   (df['unrefreshed19c'] >= (data[3] - 1)) &
                   (df['unrefreshed19c'] <= (data[3] + 1)) &
                   (df['musclepain25c'] >= (data[4] - 1)) &
                   (df['musclepain25c'] <= (data[4] + 1)) &
                   (df['bloating29c'] >= (data[5] - 1)) &
                   (df['bloating29c'] <= (data[5] + 1)) &
                   (df['remember36c'] <= (data[6] + 1)) &
                   (df['remember36c'] >= (data[6] - 1)) &
                   (df['difficulty37c'] >= (data[7] - 1)) &
                   (df['difficulty37c'] <= (data[7] + 1)) &
                   (df['bowel46c'] >= (data[8] - 1)) &
                   (df['bowel46c'] <= (data[8] + 1)) &
                   (df['unsteady48c'] >= (data[9] - 1)) &
                   (df['unsteady48c'] <= (data[9] + 1)) &
                   (df['limbs56c'] >= (data[10] - 1)) &
                   (df['limbs56c'] <= (data[10] + 1)) &
                   (df['hot58c'] >= (data[11] - 1)) &
                   (df['hot58c'] <= (data[11] + 1)) &
                   (df['flu65c'] >= (data[12] - 1)) &
                   (df['flu65c'] <= (data[12] + 1)) &
                   (df['smells66c'] >= (data[13] - 1)) &
                   (df['smells66c'] <= (data[13] + 1))]

        sample_size = len(newdf.index)
        testAcc = int(np.mean(newdf['dx'] == 1).round(decimals=2) * 100)
        user_scores = data
        cursor = mysql.connection.cursor()
        if session["checkbox"] == "data":
            cursor.execute('INSERT INTO shortform VALUES (NULL, % s, % s, % s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                           , (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9],
                            data[10], data[11], data[12], data[13]))
            mysql.connection.commit()

        mecfs_selection = probabilities.mecfs[probabilities.shortform_items]
        mecfs_14mean = mecfs_selection.mean(axis=0)
        feature_list = np.array(mecfs_selection.columns)
        categories = [*feature_list, feature_list[0]]
        print(categories)
        control_selection = probabilities.controls[probabilities.shortform_items]
        control_14mean = control_selection.mean(axis=0).drop(columns=['dx'])
        try:
            #probCFS = (np.mean(newdf.dx == 1).round(decimals=1)) * 100
            fig = go.Figure(
                data=[
                    go.Scatterpolar(r=control_14mean, theta=categories, fill='toself',
                                    name="Average Healthy Control scores"),
                    go.Scatterpolar(r=mecfs_14mean, theta=categories, fill='toself',
                                    name="Average ME/CFS scores"),
                    go.Scatterpolar(r=user_scores, theta=categories, fill='toself', name="Your scores")],
                layout=go.Layout(
                    title=go.layout.Title(text='Your scores compared with our dataset of 3,428 participants'),
                    polar={'radialaxis': {'visible': True}},
                    showlegend=True))
            fig.update_polars(radialaxis=dict(range=[0, 4]))
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            return render_template("graph.html", graphJSON=graphJSON, probCFS=testAcc, sample_size=sample_size)

        except:
            return "<h1>Unfortunately, your scores are not represented in our dataset.</h1>"
    if survey == "classic":
        import probabilities

        pemscore = session['pemscore']

        sleepscore = session['sleepscore']

        cogscore = session['cogscore']

        cursor = mysql.connection.cursor()

        #newdf = df[(df.fatigue13c == fatiguescore) & (df.minimum17c == pemscore) & (df.unrefreshed19c == sleepscore) & (
                    #df.remember36c == cogscore)]
        cursor.execute('SELECT fatigue, pem, sleep, cog FROM screen')
        results = cursor.fetchall()

        re_array = np.array(results)
        number_users = len(re_array)
        mean_array = np.mean(re_array, axis=0)
        print(mean_array)
        #new row of responeses to make categorical bins:
        user_scores = [fatiguescore, pemscore, sleepscore, cogscore]
        responses = [fatiguescore, pemscore, sleepscore, cogscore]
        newdf = df[(df['fatigue13c'] >= (responses[0]-0.5)) &
           (df['fatigue13c'] <= (responses[0] + 0.5)) &
           (df['minimum17c'] >= (responses[1] - 0.5)) &
           (df['minimum17c'] <= (responses[1] + 0.5)) &
           (df['unrefreshed19c'] >= (responses[2] - 0.5)) &
           (df['unrefreshed19c'] <= (responses[2] + 0.5)) &
           (df['remember36c'] <= (responses[3] + 0.5)) &
           (df['remember36c'] >= (responses[3] - 0.5))]

        sample_size = len(newdf.index)
        #sample_size = len(probabilities.binAccuracy(user_scores, df4=probabilities.df4))
        #testAcc = probabilities.binAccuracy(user_scores, df4=probabilities.df4).mean().round(decimals=2) * 100
        testAcc = int(np.mean(newdf['dx']==1).round(decimals=2) * 100)
        if session["checkbox"] == "data":
            cursor.execute('INSERT INTO screen VALUES (NULL, % s, % s, % s, %s)',
                           (fatiguescore, pemscore, sleepscore, cogscore))
            mysql.connection.commit()
        #past_users = np.fromiter(cursor.fetchall(), count=rows, dtype=('i4,i4,i4,i4'))
        #print(past_users)
        try:

            probCFS = (np.mean(newdf.dx == 1).round(decimals=1)) * 100
            categories = ['Fatigue', 'Post-exertional malaise', 'Sleep problems',
                                                                        'Cognitive problems']
            fig = go.Figure(
                data=[
                    go.Scatterpolar(r=probabilities.controlmean, theta=categories, fill='toself',
                                    name="Average Healthy Control scores"),
                    go.Scatterpolar(r=probabilities.combmean, theta=categories, fill='toself',
                                    name="Average ME/CFS scores"),
                    go.Scatterpolar(r=user_scores, theta=categories, fill='toself', name="Your scores")],
                layout=go.Layout(
                    title=go.layout.Title(text='Your scores compared with our dataset of 3,428 participants'),
                    polar={'radialaxis': {'visible': True}},
                    showlegend=True))
            fig.update_polars(radialaxis=dict(range=[0, 4]))
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


            print(session["checkbox"])
            return render_template("graph.html", graphJSON=graphJSON, probCFS=testAcc, sample_size=sample_size)
            #pyo.plot(fig)



        except:
            return "<h1>Unfortunately, your scores are not represented in our dataset.</h1>"
        user_score = [fatiguescore, pemscore, sleepscore, cogscore]

        fig = go.Figure(
            data=[
                go.Scatterpolar(r=probabilities.othermean, theta=probabilities.categories, fill='toself', name="Average Non-ME/CFS scores"),
                go.Scatterpolar(r=probabilities.combmean, theta=probabilities.categories, fill='toself', name="Average ME/CFS scores"),
                go.Scatterpolar(r=user_score, theta=probabilities.categories, fill='toself', name="Your scores")],
            layout=go.Layout(
                title=go.layout.Title(text='Score comparison'),
                polar={'radialaxis': {'visible': True}},
                showlegend=True))
        fig.update_polars(radialaxis=dict(range=[0, 4]))





class FreVal:
    name = "Fatigue1"
    fatigue = int





class SimpleForm(FlaskForm):
    f_options1 = RadioField('activity', choices=[
        (0, '0: none of the time'), (1, '1: a little of the time'), (2, '2: about half the time'),
        (3, '3: most of the time'), (4, '4:all of the time')],
                            coerce=int, id="todo")
    s_options1 = RadioField('s_activity', choices=[
        (0, "0:symptom not present"), (1, '1: mild'), (2, '2:moderate'), (3, '3: severe'), (4, '4:very severe')
    ], coerce=int, id="todo")
    f_options2 = RadioField('activity2', choices=[
        (0, '0: none of the time'), (1, '1: a little of the time'), (2, '2: about half the time'),
        (3, '3: most of the time'), (4, '4:all of the time')],
                            coerce=int)
    s_options2 = RadioField('s_activity2', choices=[
        (0, "0:symptom not present"), (1, '1: mild'), (2, '2:moderate'), (3, '3: severe'), (4, '4:very severe')
    ], coerce=int)
    f_options3 = RadioField('activity3', choices=[
        (0, '0: none of the time'), (1, '1: a little of the time'), (2, '2: about half the time'),
        (3, '3: most of the time'), (4, '4:all of the time')],
                            coerce=int, id="todo")
    s_options3 = RadioField('s_activity3', choices=[
        (0, "0:symptom not present"), (1, '1: mild'), (2, '2:moderate'), (3, '3: severe'), (4, '4:very severe')
    ], coerce=int)
    f_options4 = RadioField('activity4', choices=[
        (0, '0: none of the time'), (1, '1: a little of the time'), (2, '2: about half the time'),
        (3, '3: most of the time'), (4, '4:all of the time')],
                            coerce=int)
    s_options4 = RadioField('s_activity4', choices=[
        (0, "0:symptom not present"), (1, '1: mild'), (2, '2:moderate'), (3, '3: severe'), (4, '4:very severe')
    ], coerce=int)

    # next = SubmitField('Next!')
    # next2 = SubmitField("Next!")
    # next3 = SubmitField('Next!')

@app.route('/graph')
def graph(graphJSON, probCFS, sample_size):
    graphJSON = graphJSON
    probCFS = probCFS
    sample_size = sample_size
    return render_template("graph.html", graphJSON=graphJSON, probCFS=probCFS, sample_size=sample_size)

@app.route('/', methods=['post', 'get'])
def home():
    global pagenum
    global end
    form = FlaskForm()
    global survey
    session["pagenum"] = 0
    if request.method == "POST":
        session["dropdown"] = str(request.form.get("survey"))
        survey = session["dropdown"]
        session["checkbox"] = request.form.get("checkbox")
        session["pagenum"] += 1
        return redirect(url_for("page1"))
    return render_template("home.html")


@app.route('/fatigue', methods=['post', 'get'])
def page1():
    global process
    global pagenum
    global end
    global FdataMatrix
    global SdataMatrix
    form = FlaskForm()

    if request.method == "POST":

        fatiguescoref = request.form.get("fatigue")
        fatiguescores = request.form.get("severity")
        if fatiguescores is not None and fatiguescoref is not None:
            session["fatiguescoref"] = fatiguescoref
            session["fatiguescores"] = fatiguescores
            session['pagenum'] += 1
            if survey == "rf14":
                return redirect(url_for("expem1"))
            # for practice purposes, I set these thresholds to 0:
            if int(session["fatiguescoref"]) < 0 or int(session["fatiguescores"]) < 0:
                if survey == "classic":
                    end = True
                    return render_template("example4.html")
                else:
                    return redirect(url_for("page2"))
            else:
                return redirect(url_for("page2"))
        else:
            flash(message)
            return render_template("result.html", message=message, pagenum=session['pagenum'])

    return render_template("result.html", message='', pagenum=session['pagenum'])


@app.route('/minimum', methods=["post", "get"])
def page2():
    # fatiguescore = session["fatiguescore"]
    form = FlaskForm()
    global pemdomain
    if request.method == "POST":
        minexf = request.form.get("minex")
        minexs = request.form.get("minex_s")
        if minexs is not None and minexf is not None:
            session["minexf"] = int(minexf)
            session["minexs"] = int(minexs)
            session['pagenum'] += 1
            if survey == "rf14":
                return redirect(url_for("page3"))
            if int(minexs) >= 2 and int(minexf) >= 2:
                pemdomain = 1
                session['pemscore'] = (session['minexf'] + session['minexs']) / 2
                if survey == "classic" or survey == "rf4":
                    return redirect(url_for("page3"))
            else:
                if survey == "classic":
                    return redirect(url_for("expem1"))
                if survey == "rf4":
                    return redirect(url_for("page3"))
        else:
            return render_template("page2.html", pagenum=session['pagenum'], message=message)
    else:
        return render_template("page2.html", pagenum=session['pagenum'])


@app.route('/unrefreshed', methods=['post', 'get'])
def page3():
    global sleepdomain
    form = FlaskForm()
    if request.method == "POST":
        sleepf = request.form.get("sleepf")
        sleeps = request.form.get("sleeps")
        if sleeps is not None and sleepf is not None:
            session["sleepf"] = sleepf
            session["sleeps"] = sleeps
            session['pagenum'] += 1
            if survey == "rf14":
                return redirect(url_for("musclepain"))
            if int(session["sleepf"]) >= 2 and int(session["sleeps"]) >= 2:
                session['sleepscore'] = (int(session['sleepf']) + int(session['sleeps'])) / 2
                sleepdomain = 1
                if survey == "classic" or survey == "rf4":
                    return redirect(url_for("page4"))
            else:
                if survey == "classic":
                    return redirect(url_for("exsleep1"))
                if survey == "rf4":
                    return redirect(url_for("page4"))
        else:
            return render_template("page3.html", pagenum=session['pagenum'], message=message)
    return render_template("page3.html", pagenum=session['pagenum'], message='')


@app.route('/remember', methods=['post', 'get'])
def page4():
    global cogdomain
    form = FlaskForm()
    if request.method == "POST":
        rememberf = request.form.get("rememberf")
        remembers = request.form.get("remembers")
        if remembers is not None and rememberf is not None:
            session["rememberf"] = rememberf
            session["remembers"] = remembers
            session['pagenum'] += 1
            if survey == "rf14":
                return redirect(url_for("excog1"))
            else:
                if int(session["rememberf"]) >= 2 and int(session["remembers"]) >= 2:
                    cogdomain = 1
                    session['cogscore'] = (int(session['rememberf']) + int(session['remembers'])) / 2
                    if survey == "classic" or survey == "rf4":
                        end = True
                        return diagnose()
                else:
                    if survey == "rf4":
                        return diagnose()
                    if survey == "classic":
                        return redirect(url_for("excog1"))
        else:
            return render_template("page4.html", pagenum=session['pagenum'], message=message)
    return render_template("page4.html", pagenum=session['pagenum'], message='')


@app.route('/end2', methods=['get'])
def end2():
    global pagenum
    fatiguescoref = int(session["fatiguescoref"])
    fatiguescores = int(session["fatiguescores"])
    minexf = int(session["minexf"])
    minexs = int(session["minexs"])
    global pemdomain
    global cogdomain
    global sleepdomain

    sleepf = int(session["sleepf"])
    sleeps = int(session["sleeps"])
    rememberf = int(session["rememberf"])
    remembers = int(session["remembers"])


    if pemdomain == 1 and sleepdomain == 1 and cogdomain == 1:
        return f"<h1>{pemdomain}You may have ME/CFS. We advise you to consult a specialist. </h1>"
    else:
        return f"<h1>{pemdomain}You probably don't have ME/CFS</h1>"


@app.route('/soreness', methods=['post', 'get'])
def expem1():
    form = FlaskForm()
    global pemdomain
    if request.method == "POST":
        soref = request.form.get("soref")
        sores = request.form.get("sores")
        if soref is not None and sores is not None:
            session["soref"] = soref
            session["sores"] = sores
            session['pagenum'] += 1
            if survey == "rf14":
                return redirect(url_for("page2"))
            if int(session["soref"]) >= 2 and int(session["sores"]) >= 2:
                session['pemscore'] = (int(session['soref']) + int(session['sores'])) / 2
                pemdomain = 1
                if survey == "classic":
                    return redirect(url_for("page3"))
            else:
                return redirect(url_for("expem2"))
        else:
            return render_template("expem1.html", pagenum=session['pagenum'], message=message)
    return render_template("expem1.html", pagenum=session['pagenum'], message='')


@app.route('/drained', methods=['post', 'get'])
def expem2():
    form = FlaskForm()
    global pemdomain
    if request.method == "POST":
        drainedf = request.form.get("drainedf")
        draineds = request.form.get("draineds")
        if drainedf is not None and draineds is not None:
            session["drainedf"] = drainedf
            session["draineds"] = draineds
            session['pagenum'] += 1
            if int(session["drainedf"]) >= 2 and int(session["draineds"]) >= 2:
                session['pemscore'] = (int(session['drainedf']) + int(session['draineds'])) / 2
                pemdomain = 1
                return redirect(url_for("page3"))
            else:
                return redirect(url_for("expem3"))
        else:
            return render_template("expem2.html", pagenum=session['pagenum'], message=message)
    return render_template("expem2.html", pagenum=session['pagenum'], message='')


@app.route('/heavy', methods=['post', 'get'])
def expem3():
    form = FlaskForm()
    global pemdomain
    if request.method == "POST":
        heavyf = request.form.get("heavyf")
        heavys = request.form.get("heavys")
        session['pagenum'] += 1
        if heavyf is not None and heavys is not None:
            session["heavyf"] = heavyf
            session["heavys"] = heavys
            if int(session["heavyf"]) >= 2 and int(session["heavys"]) >= 2:
                session['pemscore'] = (int(session['heavyf']) + int(session['heavys'])) / 2
                pemdomain = 1
                return redirect(url_for("page3"))
            else:
                return redirect(url_for("expem4"))
        else:
            return render_template("expem3.html", pagenum=session['pagenum'], message=message)
    return render_template("expem3.html", pagenum=session['pagenum'], message='')


@app.route('/mentally', methods=['post', 'get'])
def expem4():
    form = FlaskForm()
    global pemdomain
    if request.method == "POST":
        mentalf = request.form.get("mentalf")
        mentals = request.form.get("mentals")
        if mentalf is not None and mentals is not None:
            session["mentalf"] = mentalf
            session["mentals"] = mentals
            session['pagenum'] += 1
            if int(session["mentalf"]) >= 2 and int(session["mentals"]) >= 2:
                session['pemscore'] = (int(session['mentalf']) + int(session['mentals'])) / 2
                pemdomain = 1
                return redirect(url_for("page3"))
            else:
                session['pemscore'] = (int(session['mentalf']) + int(session['mentals'])) / 2
                return redirect(url_for("page3"))
    return render_template("expem4.html", message='', pagenum=session['pagenum'])


@app.route('/staying', methods=['post', 'get'])
def exsleep1():
    form = FlaskForm()
    global sleepdomain
    if request.method == "POST":
        stayf = request.form.get("stayf")
        stays = request.form.get("stays")
        if stayf is not None and stays is not None:
            session["stayf"] = stayf
            session["stays"] = stays
            session['pagenum'] +=1
            if int(session["stayf"]) >= 2 and int(session["stays"]) >= 2:
                session['sleepscore'] = (int(session['stayf']) + int(session['stays'])) / 2
                sleepdomain = 1
                return redirect(url_for("page4"))
            else:
                return redirect(url_for("exsleep2"))
        else:
            return render_template("exsleep1.html", message=message, pagenum=session['pagenum'])
    return render_template("exsleep1.html", message='', pagenum=session['pagenum'])


@app.route('/nap', methods=['post', 'get'])
def exsleep2():
    form = FlaskForm()
    global sleepdomain
    if request.method == "POST":
        napf  = request.form.get("napf")
        naps = request.form.get("naps")
        if napf is not None and naps is not None:
            session["napf"] = napf
            session["naps"] = naps
            session['pagenum'] +=1
            if int(session["napf"]) >= 2 and int(session["naps"]) >= 2:
                session['sleepscore'] = (int(session['napf']) + int(session['naps'])) / 2
                sleepdomain = 1
                return redirect(url_for("page4"))
            else:
                return redirect(url_for("exsleep3"))
        else:
            return render_template("exsleep2.html", message=message, pagenum=session['pagenum'])
    return render_template("exsleep2.html", message='', pagenum=session['pagenum'])


@app.route('/falling', methods=['post', 'get'])
def exsleep3():
    form = FlaskForm()
    global sleepdomain
    if request.method == "POST":
        fallf  = request.form.get("fallf")
        falls = request.form.get("falls")
        if fallf is not None and falls is not None:
            session["fallf"] = fallf
            session["falls"] = falls
            session['pagenum'] += 1
            if int(session["fallf"]) >= 2 and int(session["falls"]) >= 2:
                session['sleepscore'] = (int(session['fallf']) + int(session['falls'])) / 2
                sleepdomain = 1
                return redirect(url_for("page4"))
            else:
                return redirect(url_for("exsleep4"))
        else:
            return render_template("exsleep3.html", message=message, pagenum=session['pagenum'])
    return render_template("exsleep3.html", message='', pagenum=session['pagenum'])


@app.route('/allday', methods=['post', 'get'])
def exsleep4():
    form = FlaskForm()
    if request.method == "POST":
        alldayf = request.form.get("alldayf")
        alldays = request.form.get("alldays")
        if alldayf is not None and alldays is not None:
            session["alldayf"] = alldayf
            session["alldays"] = alldays
            session['pagenum'] += 1
            if int(session["alldayf"]) >= 2 and int(session["alldays"]) >= 2:
                session['sleepscore'] = (int(session['alldayf']) + int(session['alldays'])) / 2
                sleepdomain = 1
                return redirect(url_for("page4"))
            else:
                session['sleepscore'] = (int(session['alldayf']) + int(session['alldays'])) / 2
                return redirect(url_for("page4"))
    return render_template("exsleep4.html", message='', pagenum=session['pagenum'])


@app.route('/attention', methods=['post', 'get'])
def excog1():
    form = FlaskForm()
    if request.method == "POST":
        attentionf = request.form.get("attentionf")
        attentions = request.form.get("attentions")
        if attentions is not None and attentionf is not None:
            session["attentionf"] = attentionf
            session["attentions"] = attentions
            session['pagenum'] += 1
            if survey == "rf14":
                return redirect(url_for("bowel"))
            else:
                if int(session["attentionf"]) >= 2 and int(session["attentions"]) >= 2:
                    cogdomain = 1
                    session['cogscore'] = (int(session['attentionf']) + int(session['attentions'])) / 2
                    end = True

                    return diagnose()
                else:
                    return redirect(url_for("excog2"))
        else:
            return render_template("excog1.html", message=message, pagenum=session['pagenum'])
    return render_template("excog1.html", message='', pagenum=session['pagenum'])


@app.route('/word', methods=['post', 'get'])
def excog2():
    form = FlaskForm()
    global cogdomain
    global end
    if request.method == "POST":
        wordf = request.form.get("wordf")
        words = request.form.get("words")
        if words is not None and wordf is not None:
            session["wordf"] = wordf
            session["words"] = words
            session['pagenum'] += 1
            if int(session["wordf"]) >= 2 and int(session["words"]) >= 2:
                session['cogscore'] = (int(session['wordf']) + int(session['words'])) / 2
                end = True
                cogdomain = 1
                return diagnose()
            else:
                return redirect(url_for("excog3"))
        else:
            return render_template("excog2.html", message=message, pagenum=session['pagenum'])
    return render_template("excog2.html", message='', pagenum=session['pagenum'])


@app.route('/focus', methods=['post', 'get'])
def excog3():
    form = FlaskForm()
    global end
    global cogdomain
    if request.method == "POST":
        focusf = request.form.get("focusf")
        focuss = request.form.get("focuss")
        if focuss is not None and focusf is not None:
            session["focusf"] = focusf
            session["focuss"] = focuss
            session['pagenum']+=1
            if int(session["focusf"]) >= 2 and int(session["focuss"]) >= 2:
                session['cogscore'] = (int(session['focusf']) + int(session['focuss'])) / 2
                #end = True
                cogdomain = 1
                return diagnose()
            else:
                #end = True
                cogdomain = 0
                session['cogscore'] = (int(session['focusf']) + int(session['focuss'])) / 2
                return diagnose()
        else:
            return render_template("excog3.html", message=message, pagenum=session['pagenum'])
    return render_template("excog3.html", message='', pagenum=session['pagenum'])


@app.route('/musclepain', methods=['post', 'get'])
def musclepain():
    global end
    form = FlaskForm()
    if request.method == "POST":
        musclef = request.form.get("musclef")
        mucles = request.form.get("muscles")
        if musclef is not None and mucles is not None:
            session["musclef"] = musclef
            session["muscles"] = mucles
            session['pagenum'] += 1
            return redirect(url_for("bloating"))
        else:
            return render_template("musclepain.html", message=message, pagenum=session['pagenum'])
    return render_template("musclepain.html", message='', pagenum=session['pagenum'])


@app.route('/bloating', methods=['post', 'get'])
def bloating():
    global end
    form = FlaskForm()
    if request.method == "POST":
        bloatf = request.form.get("bloatf")
        bloats = request.form.get("bloats")
        if bloats is not None and bloatf is not None:
            session["bloatf"] = bloatf
            session["bloats"] = bloats
            session['pagenum'] += 1
            return redirect(url_for("page4"))
        else:
            return render_template("bloating.html", message=message, pagenum=session['pagenum'])
    return render_template("bloating.html", message='', pagenum=session['pagenum'])

@app.route('/bowel', methods=['post', 'get'])
def bowel():
    global end
    form = FlaskForm()
    if request.method == "POST":
        bowelf = request.form.get("bowelf")
        bowels = request.form.get("bowels")
        if bowels is not None and bowelf is not None:
            session["bowelf"] = bowelf
            session["bowels"] = bowels
            session['pagenum'] += 1
            return redirect(url_for("unsteady"))
        else:
            return render_template("bowel.html", message=message, pagenum=session['pagenum'])
    return render_template("bowel.html", message='', pagenum=session['pagenum'])


@app.route('/unsteady', methods=['post', 'get'])
def unsteady():
    global end
    form = FlaskForm()
    if request.method == "POST":
        unsteadyf = request.form.get("unsteadyf")
        unsteadys = request.form.get("unsteadys")
        if unsteadyf is not None and unsteadys is not None:
            session["unsteadyf"] = unsteadyf
            session["unsteadys"] = unsteadys
            session['pagenum'] += 1
            return redirect(url_for("cold_limbs"))
        else:
            return render_template("unsteady.html", message=message, pagenum=session['pagenum'])
    return render_template("unsteady.html", message='', pagenum=session['pagenum'])

@app.route('/cold_limbs', methods=['post', 'get'])
def cold_limbs():
    global end
    form = FlaskForm()
    if request.method == "POST":
        limbsf = request.form.get("limbsf")
        limbss = request.form.get("limbss")
        if limbsf is not None and limbss is not None:
            session["limbsf"] = limbsf
            session["limbss"] = limbss
            session['pagenum'] += 1
            return redirect(url_for("hot_cold"))
        else:
            return render_template("limbs.html", message=message, pagenum=session['pagenum'])
    return render_template("limbs.html", message='', pagenum=session['pagenum'])

@app.route('/hot_cold', methods=['post', 'get'])
def hot_cold():
    global end
    form = FlaskForm()
    if request.method == "POST":
        hotf  = request.form.get("hotf")
        hots = request.form.get("hots")
        if hotf is not None and hots is not None:
            session["hotf"] = hotf
            session["hots"] = hots
            session['pagenum'] += 1
            return redirect(url_for("flu"))
        else:
            return render_template("hot.html", message=message, pagenum=session['pagenum'])
    return render_template("hot.html", message='', pagenum=session['pagenum'])

@app.route('/flu', methods=['post', 'get'])
def flu():
    global end
    form = FlaskForm()
    if request.method == "POST":
        fluf  = request.form.get("fluf")
        flus = request.form.get("flus")
        if fluf is not None and flus is not None:
            session["fluf"] = fluf
            session["flus"] = flus
            session['pagenum'] += 1
            return redirect(url_for("smells"))
        else:
            return render_template("flu.html", message=message, pagenum=session['pagenum'])
    return render_template("flu.html", message='', pagenum=session['pagenum'])

@app.route('/smells', methods=['post', 'get'])
def smells():
    global end
    form = FlaskForm()
    if request.method == "POST":
        smellf = request.form.get("smellf")
        smells = request.form.get("smells")
        if smellf is not None and smells is not None:
            session["smellf"] = smellf
            session["smells"] = smells
            session['pagenum'] += 1
            return diagnose()
        else:
            return render_template("smells.html", message=message, pagenum=session['pagenum'])
    return render_template("smells.html", message='', pagenum=session['pagenum'])


@app.route('/end', methods=['post', 'get'])
def end():
    form = FlaskForm()
    if request.method == "POST":
        return redirect(url_for('home'))
    # return render_template("example4.html")

    if end:
        fatiguedata = ((int(session["fatiguescoref"]) + int(session['fatiguescores'])) / 2)
        minexdata = ((int(session["minexf"]) + int(session['minexs'])) / 2)
        sleepdata = ((int(session["sleepf"]) + int(session['sleeps'])) / 2)
        cogdata = ((int(session["rememberf"]) + int(session['remembers'])) / 2)
        # data = [fatiguedata, minexdata, sleepdata, cogdata]
        data = np.array([[fatiguedata, minexdata, sleepdata, cogdata]])
        #result = randomForest.rf2.predict(data)
        #if result[0] == 1:
            #return f"The random forest model classifies your responses with the ME/CFS group. Model accuracy is {randomForest.accuracy}"
        #else:
            #return f"The random forest model does not predict ME/CFS. Model accuracy is {randomForest.accuracy}"

        # return f"{result}"


@app.route('/about', methods=['post', 'get'])
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
