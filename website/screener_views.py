from flask import Blueprint, render_template, session, request, redirect, url_for
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.utils
import numpy as np
screener_views = Blueprint('screener_views', __name__)

from website import mysql
message = "Please enter a response for both frequency and severity before continuing"

@screener_views.route('/home', methods=['post', 'get'])
def home():
    session["pagenum"] = 0
    survey = 'classic'
    if request.method == "POST":
        session["pagenum"] += 1
        return redirect(url_for("screener_views.page1"))
    return render_template("home.html", session=session)



# First symptom question
@screener_views.route('/fatigue', methods=['post', 'get'])
def page1():
    global message
    error = None

    session['pagenum'] = 1
    if request.method == "POST":
        selected_radio = request.form.get('fatigue')
        selected_severity = request.form.get('severity')
        fatiguescoref = request.form.get("fatigue")
        fatiguescores = request.form.get("severity")
        if fatiguescores is not None and fatiguescoref is not None:
            session["fatiguescoref"] = fatiguescoref
            session["fatiguescores"] = fatiguescores
            session['pagenum'] += 1

            return redirect(url_for("screener_views.page2"))
        else:
            error=message
            return render_template("result.html", error=message, pagenum=session['pagenum'],
                                   selected_radio=selected_radio, selected_severity=selected_severity)
    return render_template("result.html", error=error, pagenum=session['pagenum'])


@screener_views.route('/minimum', methods=["post", "get"])
def page2():
    # fatiguescore = session["fatiguescore"]

    global pemname
    selected_f = request.form.get('minex')
    selected_s = request.form.get('minex_s')
    error = None
    if request.method == "POST":
        minexf = request.form.get("minex")
        minexs = request.form.get("minex_s")
        if minexs is not None and minexf is not None:
            session["minexf"] = int(minexf)
            session["minexs"] = int(minexs)
            session["pemscore"] = (int(minexf) + int(minexs)) / 2
            session["pemname"] = "minimum17"
            session['pagenum'] += 1

            return redirect(url_for("screener_views.page3"))

        else:
            return render_template("page2.html", pagenum=session['pagenum'], error=message,
                                   selected_s=selected_s, selected_f=selected_f)
    else:
        return render_template("page2.html", error=error, pagenum=session['pagenum'])


@screener_views.route('/unrefreshed', methods=['post', 'get'])
def page3():
    global sleepname

    if request.method == "POST":
        sleepf = request.form.get("sleepf")
        sleeps = request.form.get("sleeps")
        if sleeps is not None and sleepf is not None:
            session["sleepf"] = sleepf
            session["sleeps"] = sleeps
            session['pagenum'] += 1

            if int(session["sleepf"]) >= 0 and int(session["sleeps"]) >= 0:
                session['sleepscoref'] = int(sleepf)
                session['sleepscores'] = int(sleeps)
                session['sleepscore'] = (int(session['sleepf']) + int(session['sleeps'])) / 2
                session["sleepname"] = 'unrefreshed19'

                return redirect(url_for("screener_views.page4"))

        else:
            return render_template("page3.html", pagenum=session['pagenum'], message=message,
                                   sleepf=sleepf, sleeps=sleeps)
    return render_template("page3.html", pagenum=session['pagenum'], message='')


@screener_views.route('/remember', methods=['post', 'get'])
def page4():
    global cogname

    if request.method == "POST":
        rememberf = request.form.get("rememberf")
        remembers = request.form.get("remembers")
        if remembers is not None and rememberf is not None:
            session["rememberf"] = rememberf
            session["remembers"] = remembers
            session['pagenum'] += 1

            session['cogscoref'] = int(rememberf)
            session['cogscores'] = int(remembers)
            session["cogname"] = 'remember36'
            session['cogscore'] = (int(session['rememberf']) + int(session['remembers'])) / 2

            return redirect(url_for('screener_views.reduction'))

        else:
            return render_template("page4.html", pagenum=session['pagenum'], message=message,
                                   rememberf=rememberf, remembers=remembers)
    return render_template("page4.html", pagenum=session['pagenum'], message='')


@screener_views.route('/reduction', methods=['post', 'get'])
def reduction():
    msg_reduction = "Please select one of the options before continuing"
    if request.method == 'POST':
        reduction = request.form.get('reduction')
        if reduction is not None:
            session['reduction'] = reduction
            return redirect(url_for('screener_views.graph'))
        else:
            return render_template("reduction.html", message=msg_reduction, pagenum=session['pagenum'])
    return render_template('reduction.html', message='', pagenum=session['pagenum'])


@screener_views.route('/graph')
def graph():
    fatiguescore = (int(session["fatiguescoref"]) +
                    int(session["fatiguescores"])) / 2
    pemscore = session['pemscore']

    sleepscore = session['sleepscore']

    cogscore = session['cogscore']

    reduction = session['reduction']

    df = pd.read_csv('MECFS COMPOSITE DATA.csv')
    responses = [fatiguescore, pemscore, sleepscore, cogscore]
    iomfatiguecheck = "No"
    iomreductioncheck = "No"
    iompemcheck = "No"
    iomsleepcheck = "No"
    iomcogcheck = "No"
    if int(session['fatiguescoref']) >= 2 and int(session['fatiguescores']) >= 2:
        iomfatiguecheck = "Yes"
    if int(session['reduction']) == 1:
        iomreductioncheck = "Yes"
    if int(session['minexf']) >= 2 and int(session['minexs']) >= 2:
        iompemcheck = "Yes"
    if int(session['sleepf']) >= 2 and int(session['sleeps']) >= 2:
        iomsleepcheck = "Yes"
    if int(session['rememberf']) and int(session['remembers']) >= 2:
        iomcogcheck = "Yes"

    if iomfatiguecheck == "Yes" and iomreductioncheck == "Yes" and iompemcheck == "Yes" and iomsleepcheck == "Yes" and iomcogcheck == "Yes":
        iom_msg = "Your answers indicate you may meet the IOM Criteria for ME/CFS. To compare your" \
                  " scores with more case definitions, continue to the next section"
        iomdxcheck = "Met"

    else:
        iom_msg = 'Your responses do not meet the IOM Criteria for ME/CFS. To assess more case definitions, ' \
                  'continue to the next section'
        iomdxcheck = "Not met"

    if session["checkbox"] == "data" and session['logged_in']:
        user_id = int(session['user_id'])
        print(user_id)
        cursor = mysql.connection.cursor()
        if session['logged_in'] == True:
            if 'user_id' in session:
                login_id = session['user_id']
            else:
                # get the next auto-increment id value from the login table
                cursor.execute(
                    "SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'dsq_screener' AND TABLE_NAME = 'login'")
                result = cursor.fetchone()
                login_id = result[0]

                # insert a new row into the login table to reserve the id value
                cursor.execute("INSERT INTO login (id) VALUES (NULL)")
                mysql.connection.commit()
                cursor.execute("""
                         INSERT INTO screen (fatigue13f, fatigue13s, minimum17f, minimum17s, unrefreshed19f, unrefreshed19s,
                                             remember36f, remember36s, reduction, login_id)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                         """, (int(session['fatiguescoref']), int(session['fatiguescores']), int(session['minexf']),
                               int(session['minexs']),
                               int(session['sleepf']), int(session['sleeps']), int(session['rememberf']),
                               int(session['remembers']),
                               int(session['reduction']), login_id))
                mysql.connection.commit()

    composite_scores = responses
    categories = ['Fatigue', 'Post-exertional malaise', 'Sleep problems',
                  'Cognitive problems']

    select_list = ['fatigue13c', (session['pemname'] + 'c'),
                   (session['cogname'] + 'c'), (session['sleepname'] + 'c'), 'dx']
    df = df[select_list]

    fig = go.Figure(
        data=[
            go.Bar(y=composite_scores, x=categories, name="Your scores"),
            go.Bar(y=np.mean(df[(df['dx'] == 1)], axis=0), x=categories,
                   name="Average ME/CFS scores")],
        layout=go.Layout(
            title=go.layout.Title(text='Your scores compared'
                                       ' with our dataset of 2,402 participants'),
            showlegend=True, legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1)))
    fig.update_layout(yaxis_title='Averaged Frequency and Severity Scores',
                      xaxis_title='Symptom Domains')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    print(session["checkbox"])

    return render_template("graph.html",
                                   iomfatiguecheck=iomfatiguecheck, iomreductioncheck=iomreductioncheck,
                                   iompemcheck=iompemcheck, iomdxcheck=iomdxcheck,
                                   iomsleepcheck=iomsleepcheck, iomcogcheck=iomcogcheck,
                                   next_link="Continue to full DSQ", graphJSON=graphJSON, iom_msg=iom_msg)