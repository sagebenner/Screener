import numpy as np
import plotly.utils
from flask import Flask, render_template, request, redirect, url_for, session
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

def diagnose():
    global end
    df = pd.read_csv('MECFS VS OTHERS BINARY.csv')

    fatiguescore = (int(session["fatiguescoref"]) + int(session["fatiguescores"])) / 2

    if survey == "rf4":
        import randomForest
        pemscore = (int(session["minexf"]) + int(session["minexf"])) / 2
        sleepscore = (int(session["sleepf"]) + int(session["sleeps"])) / 2
        cogscore = (int(session["rememberf"]) + int(session["remembers"])) / 2
        data = np.array([[fatiguescore, pemscore, sleepscore, cogscore]])
        result = randomForest.rf.predict(data)
        if result[0] == 1:
            return f"<h1>The random forest model predicts ME/CFS. Model accuracy is {randomForest.accuracy.round(decimals=2)}</h1>"
        else:
            return f"<h1>The random forest model does NOT predict ME/CFS. Model accuracy is {randomForest.accuracy.round(decimals=2)}</h1>"
    if survey == "rf14":
        import randomForest
        pemscore = (int(session["minexf"]) + int(session["minexs"])) / 2
        sleepscore = (int(session["sleepf"]) + int(session["sleeps"])) / 2
        cogscore = (int(session["rememberf"]) + int(session["remembers"])) / 2
        df = pd.read_csv('MECFS VS OTHERS BINARY.csv')
        data = np.array([[fatiguescore, ((int(session["soref"]) + int(session["sores"])) / 2), pemscore,
                          ((int(session["sleepf"]) + int(session["sleeps"])) / 2),
                          ((int(session["musclef"]) + int(session["muscles"])) / 2),
                          ((int(session["bloatf"]) + int(session["bloats"])) / 2), cogscore,
                          ((int(session["attentionf"]) + int(session["attentions"])) / 2),
                          ((int(session["bowelf"]) + int(session["bowels"])) / 2),
                          ((int(session["unsteadyf"]) + int(session["unsteadys"])) / 2),
                          ((int(session["limbsf"]) + int(session["limbss"])) / 2),
                          ((int(session["hotf"]) + int(session["hots"])) / 2),
                          ((int(session["fluf"]) + int(session["flus"])) / 2),
                          ((int(session["smellf"]) + int(session["smells"])) / 2)]])
        result = randomForest.rf2.predict(data)
        if result[0] == 1:
            return f"<h1>The random forest model predicts ME/CFS. Model accuracy is {randomForest.accuracy2.round(decimals=12)}</h1>"
        else:
            return f"<h1>The random forest model does NOT predict ME/CFS. Model accuracy is {randomForest.accuracy2.round(decimals=2)}</h1>"
    if survey == "classic":
        #import probabilities
        if "minexs" and "minexf" in session:
            pemscore = (int(session["minexf"]) + int(session["minexs"])) / 2

        sleepscore = (int(session["sleepf"]) + int(session["sleeps"])) / 2
        cogscore = (int(session["rememberf"]) + int(session["remembers"])) / 2

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
        testAcc = np.mean(newdf['dx']==1).round(decimals=2) * 100
        if session["checkbox"] == "data":
            cursor.execute('INSERT INTO screen VALUES (NULL, % s, % s, % s, %s)',
                           (fatiguescore, pemscore, sleepscore, cogscore))
            mysql.connection.commit()
        #past_users = np.fromiter(cursor.fetchall(), count=rows, dtype=('i4,i4,i4,i4'))
        #print(past_users)
        try:
            probCFS = (np.mean(newdf.dx == 1).round(decimals=1)) * 100

            fig = go.Figure(
                data=[
                    go.Scatterpolar(r=probabilities.controlmean, theta=probabilities.categories, fill='toself',
                                    name="Average Healthy Control scores"),
                    go.Scatterpolar(r=probabilities.combmean, theta=probabilities.categories, fill='toself',
                                    name="Average ME/CFS scores"),
                    go.Scatterpolar(r=user_scores, theta=probabilities.categories, fill='toself', name="Your scores")],
                layout=go.Layout(
                    title=go.layout.Title(text='Your scores compared with our dataset of 3,428 participants'),
                    polar={'radialaxis': {'visible': True}},
                    showlegend=True))
            fig.update_polars(radialaxis=dict(range=[0, 4]))
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            fig2 = go.Figure(
                data=[
                    go.Scatterpolar(r=mean_array, theta=probabilities.categories, fill='toself',
                                    name="Average scores from other users"),
                    go.Scatterpolar(r=user_scores, theta=probabilities.categories, fill='toself', name="Your scores")],
                layout=go.Layout(
                    title=go.layout.Title(text=f"Average scores from other users ({number_users})"),
                    polar={'radialaxis': {'visible': True}},
                    showlegend=True))
            fig2.update_polars(radialaxis=dict(range=[0, 4]))
            graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            print(session["checkbox"])
            return render_template("graph.html", graphJSON=graphJSON, probCFS=testAcc, sample_size=sample_size,
                                   graphJSON2=graphJSON2)
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
    if request.method == "POST":
        session["dropdown"] = str(request.form.get("survey"))
        survey = session["dropdown"]
        session["checkbox"] = request.form.get("checkbox")
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
        session["fatiguescoref"] = fatiguescoref
        session["fatiguescores"] = fatiguescores
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
        return render_template("result.html")


@app.route('/minimum', methods=["post", "get"])
def page2():
    # fatiguescore = session["fatiguescore"]
    form = FlaskForm()
    global pemdomain
    if request.method == "POST":
        session["minexf"] = request.form.get("minex")
        session["minexs"] = request.form.get("minex_s")
        minexf = int(session["minexf"])
        minexs = int(session["minexs"])
        if survey == "rf14":
            return redirect(url_for("page3"))
        if minexs >= 2 and minexf >= 2:
            pemdomain = 1
            if survey == "classic" or survey == "rf4":
                return redirect(url_for("page3"))
        else:
            if survey == "classic":
                return redirect(url_for("expem1"))
            if survey == "rf4":
                return redirect(url_for("page3"))

    return render_template("page2.html")


@app.route('/unrefreshed', methods=['post', 'get'])
def page3():
    global sleepdomain
    form = FlaskForm()
    if request.method == "POST":
        sleepf = request.form.get("sleepf")
        sleeps = request.form.get("sleeps")
        session["sleepf"] = sleepf
        session["sleeps"] = sleeps
        if survey == "rf14":
            return redirect(url_for("musclepain"))
        if int(session["sleepf"]) >= 2 and int(session["sleeps"]) >= 2:
            sleepdomain = 1
            if survey == "classic" or survey == "rf4":
                return redirect(url_for("page4"))
        else:
            if survey == "classic":
                return redirect(url_for("exsleep1"))
            if survey == "rf4":
                return redirect(url_for("page4"))
    return render_template("page3.html")


@app.route('/remember', methods=['post', 'get'])
def page4():
    global cogdomain
    form = FlaskForm()
    if request.method == "POST":
        rememberf = request.form.get("rememberf")
        remembers = request.form.get("remembers")
        session["rememberf"] = rememberf
        session["remembers"] = remembers
        if survey == "rf14":
            return redirect(url_for("excog1"))
        else:
            if int(session["rememberf"]) >= 2 and int(session["remembers"]) >= 2:
                cogdomain = 1
                if survey == "classic" or survey == "rf4":
                    end = True
                    return diagnose()
            else:
                if survey == "rf4":
                    return diagnose()
                if survey == "classic":
                    return redirect(url_for("excog1"))
    return render_template("page4.html")


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
        session["soref"] = soref
        session["sores"] = sores
        if survey == "rf14":
            return redirect(url_for("page2"))
        if int(session["soref"]) >= 2 and int(session["sores"]) >= 2:
            pemdomain = 1
            return redirect(url_for("page3"))
        else:
            return redirect(url_for("expem2"))
    return render_template("expem1.html")


@app.route('/drained', methods=['post', 'get'])
def expem2():
    form = FlaskForm()
    global pemdomain
    if request.method == "POST":
        session["drainedf"] = request.form.get("drainedf")
        session["draineds"] = request.form.get("draineds")
        if int(session["drainedf"]) >= 2 and int(session["draineds"]) >= 2:
            pemdomain = 1
            return redirect(url_for("page3"))
        else:
            return redirect(url_for("expem3"))
    return render_template("expem2.html")


@app.route('/heavy', methods=['post', 'get'])
def expem3():
    form = FlaskForm()
    global pemdomain
    if request.method == "POST":
        session["heavyf"] = request.form.get("heavyf")
        session["heavys"] = request.form.get("heavys")
        if int(session["heavyf"]) >= 2 and int(session["heavys"]) >= 2:
            pemdomain = 1
            return redirect(url_for("page3"))
        else:
            return redirect(url_for("expem4"))
    return render_template("expem3.html")


@app.route('/mentally', methods=['post', 'get'])
def expem4():
    form = FlaskForm()
    global pemdomain
    if request.method == "POST":
        session["mentalf"] = request.form.get("mentalf")
        session["mentals"] = request.form.get("mentals")
        if int(session["mentalf"]) >= 2 and int(session["mentals"]) >= 2:
            pemdomain = 1
            return redirect(url_for("page3"))
        else:
            return redirect(url_for("page3"))
    return render_template("expem4.html")


@app.route('/staying', methods=['post', 'get'])
def exsleep1():
    form = FlaskForm()
    global sleepdomain
    if request.method == "POST":
        session["stayf"] = request.form.get("stayf")
        session["stays"] = request.form.get("stays")
        if int(session["stayf"]) >= 2 and int(session["stays"]) >= 2:
            sleepdomain = 1
            return redirect(url_for("page4"))
        else:
            return redirect(url_for("exsleep2"))
    return render_template("exsleep1.html")


@app.route('/nap', methods=['post', 'get'])
def exsleep2():
    form = FlaskForm()
    global sleepdomain
    if request.method == "POST":
        session["napf"] = request.form.get("napf")
        session["naps"] = request.form.get("naps")
        if int(session["napf"]) >= 2 and int(session["naps"]) >= 2:
            sleepdomain = 1
            return redirect(url_for("page4"))
        else:
            return redirect(url_for("exsleep3"))
    return render_template("exsleep2.html")


@app.route('/falling', methods=['post', 'get'])
def exsleep3():
    form = FlaskForm()
    global sleepdomain
    if request.method == "POST":
        session["fallf"] = request.form.get("fallf")
        session["falls"] = request.form.get("falls")
        if int(session["fallf"]) >= 2 and int(session["falls"]) >= 2:
            sleepdomain = 1
            return redirect(url_for("page4"))
        else:
            return redirect(url_for("exsleep4"))
    return render_template("exsleep3.html")


@app.route('/allday', methods=['post', 'get'])
def exsleep4():
    form = FlaskForm()
    if request.method == "POST":
        session["alldayf"] = request.form.get("alldayf")
        session["alldays"] = request.form.get("alldays")
        if int(session["alldayf"]) >= 2 and int(session["alldays"]) >= 2:
            sleepdomain = 1
            return redirect(url_for("page4"))
        else:
            return redirect(url_for("page4"))
    return render_template("exsleep4.html")


@app.route('/attention', methods=['post', 'get'])
def excog1():
    form = FlaskForm()
    if request.method == "POST":
        session["attentionf"] = request.form.get("attentionf")
        session["attentions"] = request.form.get("attentions")
        if survey == "rf14":
            return redirect(url_for("bowel"))
        else:
            if int(session["attentionf"]) >= 2 and int(session["attentions"]) >= 2:
                cogdomain = 1
                end = True

                return diagnose()
            else:
                return redirect(url_for("excog2"))
    return render_template("excog1.html")


@app.route('/word', methods=['post', 'get'])
def excog2():
    form = FlaskForm()
    global cogdomain
    global end
    if request.method == "POST":
        session["wordf"] = request.form.get("wordf")
        session["words"] = request.form.get("words")
        if int(session["wordf"]) >= 2 and int(session["words"]) >= 2:
            end = True
            cogdomain = 1
            return diagnose()
        else:
            return redirect(url_for("excog3"))
    return render_template("excog2.html")


@app.route('/focus', methods=['post', 'get'])
def excog3():
    form = FlaskForm()
    global end
    global cogdomain
    if request.method == "POST":
        session["focusf"] = request.form.get("focusf")
        session["focuss"] = request.form.get("focuss")
        if int(session["focusf"]) >= 2 and int(session["focuss"]) >= 2:
            #end = True
            cogdomain = 1
            return diagnose()
        else:
            #end = True
            cogdomain = 0
            return diagnose()

    return render_template("excog3.html")


@app.route('/musclepain', methods=['post', 'get'])
def musclepain():
    global end
    form = FlaskForm()
    if request.method == "POST":
        session["musclef"] = request.form.get("musclef")
        session["muscles"] = request.form.get("muscles")
        return redirect(url_for("bloating"))

    return render_template("musclepain.html")


@app.route('/bloating', methods=['post', 'get'])
def bloating():
    global end
    form = FlaskForm()
    if request.method == "POST":
        session["bloatf"] = request.form.get("bloatf")
        session["bloats"] = request.form.get("bloats")
        return redirect(url_for("page4"))

    return render_template("bloating.html")


@app.route('/bowel', methods=['post', 'get'])
def bowel():
    global end
    form = FlaskForm()
    if request.method == "POST":
        session["bowelf"] = request.form.get("bowelf")
        session["bowels"] = request.form.get("bowels")
        return redirect(url_for("unsteady"))

    return render_template("bowel.html")


@app.route('/unsteady', methods=['post', 'get'])
def unsteady():
    global end
    form = FlaskForm()
    if request.method == "POST":
        session["unsteadyf"] = request.form.get("unsteadyf")
        session["unsteadys"] = request.form.get("unsteadys")
        return redirect(url_for("cold_limbs"))

    return render_template("unsteady.html")

@app.route('/cold_limbs', methods=['post', 'get'])
def cold_limbs():
    global end
    form = FlaskForm()
    if request.method == "POST":
        session["limbsf"] = request.form.get("limbsf")
        session["limbss"] = request.form.get("limbss")
        return redirect(url_for("hot_cold"))

    return render_template("limbs.html")

@app.route('/hot_cold', methods=['post', 'get'])
def hot_cold():
    global end
    form = FlaskForm()
    if request.method == "POST":
        session["hotf"] = request.form.get("hotf")
        session["hots"] = request.form.get("hots")
        return redirect(url_for("flu"))

    return render_template("hot.html")

@app.route('/flu', methods=['post', 'get'])
def flu():
    global end
    form = FlaskForm()
    if request.method == "POST":
        session["fluf"] = request.form.get("fluf")
        session["flus"] = request.form.get("flus")
        return redirect(url_for("smells"))

    return render_template("flu.html")

@app.route('/smells', methods=['post', 'get'])
def smells():
    global end
    form = FlaskForm()
    if request.method == "POST":
        session["smellf"] = request.form.get("smellf")
        session["smells"] = request.form.get("smells")
        return diagnose()

    return render_template("smells.html")


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


if __name__ == '__main__':
    app.run(debug=True)
