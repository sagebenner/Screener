import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
import pandas as pd
#from wtforms.validators import InputRequired

import randomForest

#df = pd.read_csv('MECFS VS OTHERS BINARY.csv')

SECRET_KEY = 'development'

symptom = ["Fatigue", "Minimum exercise", "Sleep", "Remember"]
pagelist = ["example.html", "example2.html", "example3.html", "example4.html"]
pagenum = 0
end = False
pemdomain = 0
sleepdomain = 0
cogdomain = 0
survey = str

def summ(num1, *args):
    total = num1
    for num in args:
        total = total + num
    total = int(total)
    return total

def diagnose():
    global end
    df = pd.read_csv('MECFS VS OTHERS BINARY.csv')
    #if cogdomain==1 and pemdomain==1 and sleepdomain==1:
        #end = True
        #return render_template("example3.html")
    #else:
        #if end == True:
            #return render_template("example4.html")
        #else:
            #return redirect(url_for(next))
    fatiguescore = (int(session["fatiguescoref"]) + int(session["fatiguescores"]))/2
    pemscore = (int(session["minexf"]) + int(session["minexf"]))/2
    sleepscore = (int(session["sleepf"]) + int(session["sleeps"]))/2
    cogscore = (int(session["rememberf"]) + int(session["remembers"])) / 2

    if survey=="rf4":
        data = np.array([[fatiguescore, pemscore, sleepscore, cogscore]])
        result = randomForest.rf2.predict(data)
        if result[0] == 1:
            return f"<h1>The random forest model predicts ME/CFS. Model accuracy is {randomForest.accuracy.round(decimals=2)}</h1>"
        else:
            return f"<h1>The random forest model does NOT predict ME/CFS. Model accuracy is {randomForest.accuracy.round(decimals=2)}</h1>"

    if survey=="classic":
        newdf = df[(df.fatigue13c == fatiguescore) & (df.minimum17c == pemscore) & (df.unrefreshed19c == sleepscore) & (df.remember36c == cogscore)]
        probCFS = (np.mean(newdf.dx == 1).round(decimals=2)) * 100
    #probCFS = np.mean(probCFS)
        return f"<h1>Your probability of having ME/CFS is {probCFS} %</h1>"

class FreVal:
    name = "Fatigue1"
    fatigue = int


app = Flask(__name__)
process = []
app.config.from_object(__name__)


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

    #next = SubmitField('Next!')
    #next2 = SubmitField("Next!")
    #next3 = SubmitField('Next!')

@app.route('/', methods=['post', 'get'])
def home():
    global pagenum
    global end
    form = FlaskForm()
    global survey
    if request.method=="POST":
        session["dropdown"] = str(request.form.get("survey"))
        survey = session["dropdown"]

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

    if request.method== "POST":
        fatiguescoref = request.form.get("fatigue")
        fatiguescores = request.form.get("severity")
        session["fatiguescoref"] = fatiguescoref
        session["fatiguescores"] = fatiguescores
        if int(session["fatiguescoref"]) < 2 or int(session["fatiguescores"]) < 2:
            if survey=="classic":
                end=True
                return render_template("example4.html")
            else:
                return redirect(url_for("page2"))
        else:
            return redirect(url_for("page2"))

    else:
        return render_template("result.html")



@app.route('/minimum', methods=["post", "get"])
def page2():
    #fatiguescore = session["fatiguescore"]
    form = FlaskForm()
    global pemdomain
    if request.method=="POST":
        session["minexf"] = request.form.get("minex")
        session["minexs"] = request.form.get("minex_s")
        minexf =int(session["minexf"])
        minexs =int(session["minexs"])
        if minexs>=2 and minexf>=2:
            pemdomain=1
            if survey=="classic" or survey=="rf4":
                return redirect(url_for("page3"))
        else:
            if survey == "classic":
                return redirect(url_for("expem1"))
            if survey=="rf4":
                return redirect(url_for("page3"))

    return render_template("page2.html")



@app.route('/unrefreshed', methods=['post', 'get'])
def page3():
    global sleepdomain
    form = FlaskForm()
    if request.method=="POST":
        sleepf = request.form.get("sleepf")
        sleeps = request.form.get("sleeps")
        session["sleepf"] = sleepf
        session["sleeps"] = sleeps
        if int(session["sleepf"])>=2 and int(session["sleeps"])>=2:
            sleepdomain=1
            if survey=="classic" or survey=="rf4":
                return redirect(url_for("page4"))
        else:
            if survey=="classic":
                return redirect(url_for("exsleep1"))
            if survey=="rf4":
                return redirect(url_for("page4"))
    return render_template("page3.html")

@app.route('/remember', methods=['post', 'get'])
def page4():
    global cogdomain
    form = FlaskForm()
    if request.method=="POST":
        rememberf = request.form.get("rememberf")
        remembers = request.form.get("remembers")
        session["rememberf"] = rememberf
        session["remembers"] = remembers
        if int(session["rememberf"])>=2 and int(session["remembers"])>=2:
            cogdomain=1
            if survey=="classic" or survey=="rf4":
                end = True
                return diagnose()
        else:
            if survey=="rf4":
                return diagnose()
            if survey=="classic":
                return redirect(url_for("excog1"))
    return render_template("page4.html")

@app.route('/end2', methods=['get'])
def end2():
    global pagenum
    fatiguescoref=int(session["fatiguescoref"])
    fatiguescores=int(session["fatiguescores"])
    minexf = int(session["minexf"])
    minexs = int(session["minexs"])
    global pemdomain
    global cogdomain
    global sleepdomain

    sleepf = int(session["sleepf"])
    sleeps = int(session["sleeps"])
    rememberf = int(session["rememberf"])
    remembers = int(session["remembers"])
    tally = summ(fatiguescoref, fatiguescores, minexs, minexf, sleepf, sleeps,remembers,rememberf)


    if pemdomain == 1 and sleepdomain==1 and cogdomain==1:
            return f"<h1>{pemdomain}You may have ME/CFS. We advise you to consult a specialist. </h1>"
    else:
        return f"<h1>{pemdomain}You probably don't have ME/CFS</h1>"



@app.route('/soreness', methods = ['post', 'get'])
def expem1():
    form = FlaskForm()
    global pemdomain
    if request.method == "POST":
        soref = request.form.get("soref")
        sores = request.form.get("sores")
        session["soref"] = soref
        session["sores"] = sores
        if int(session["soref"])>=2 and int(session["sores"])>=2:
            pemdomain=1
            return redirect(url_for("page3"))
        else:
            return redirect(url_for("expem2"))
    return render_template("expem1.html")

@app.route('/drained', methods = ['post', 'get'])
def expem2():
    form = FlaskForm()
    global pemdomain
    if request.method == "POST":
        session["drainedf"] = request.form.get("drainedf")
        session["draineds"] = request.form.get("draineds")
        if int(session["drainedf"])>=2 and int(session["draineds"])>=2:
            pemdomain=1
            return redirect(url_for("page3"))
        else:
            return redirect(url_for("expem3"))
    return render_template("expem2.html")

@app.route('/heavy', methods = ['post', 'get'])
def expem3():
    form = FlaskForm()
    global pemdomain
    if request.method == "POST":
        session["heavyf"] = request.form.get("heavyf")
        session["heavys"] = request.form.get("heavys")
        if int(session["heavyf"])>=2 and int(session["heavys"])>=2:
            pemdomain=1
            return redirect(url_for("page3"))
        else:
            return redirect(url_for("expem4"))
    return render_template("expem3.html")

@app.route('/mentally', methods = ['post', 'get'])
def expem4():
    form = FlaskForm()
    global pemdomain
    if request.method == "POST":
        session["mentalf"] = request.form.get("mentalf")
        session["mentals"] = request.form.get("mentals")
        if int(session["mentalf"])>=2 and int(session["mentals"])>=2:
            pemdomain=1
            return redirect(url_for("page3"))
        else:
            return render_template("example4.html")
    return render_template("expem4.html")

@app.route('/staying', methods = ['post', 'get'])
def exsleep1():
    form = FlaskForm()
    global sleepdomain
    if request.method == "POST":
        session["stayf"] = request.form.get("stayf")
        session["stays"] = request.form.get("stays")
        if int(session["stayf"])>=2 and int(session["stays"])>=2:
            sleepdomain=1
            return redirect(url_for("page4"))
        else:
            return redirect(url_for("exsleep2"))
    return render_template("exsleep1.html")

@app.route('/nap', methods = ['post', 'get'])
def exsleep2():
    form = FlaskForm()
    global sleepdomain
    if request.method == "POST":
        session["napf"] = request.form.get("napf")
        session["naps"] = request.form.get("naps")
        if int(session["napf"])>=2 and int(session["naps"])>=2:
            sleepdomain=1
            return redirect(url_for("page4"))
        else:
            return redirect(url_for("exsleep3"))
    return render_template("exsleep2.html")


@app.route('/falling', methods = ['post', 'get'])
def exsleep3():
    form = FlaskForm()
    global sleepdomain
    if request.method == "POST":
        session["fallf"] = request.form.get("fallf")
        session["falls"] = request.form.get("falls")
        if int(session["fallf"])>=2 and int(session["falls"])>=2:
            sleepdomain=1
            return redirect(url_for("page4"))
        else:
            return redirect(url_for("exsleep4"))
    return render_template("exsleep3.html")


@app.route('/allday', methods = ['post', 'get'])
def exsleep4():
    form = FlaskForm()
    if request.method == "POST":
        session["alldayf"] = request.form.get("alldayf")
        session["alldays"] = request.form.get("alldays")
        if int(session["alldayf"])>=2 and int(session["alldays"])>=2:
            sleepdomain=1
            return redirect(url_for("page4"))
        else:
            return redirect(url_for("end"))
    return render_template("exsleep4.html")

@app.route('/attention', methods = ['post', 'get'])
def excog1():
    form = FlaskForm()
    if request.method == "POST":
        session["attentionf"] = request.form.get("attentionf")
        session["attentions"] = request.form.get("attentions")
        if int(session["attentionf"])>=2 and int(session["attentions"])>=2:
            end=True
            cogdomain=1
            return diagnose("end")
        else:
            return redirect(url_for("excog2"))
    return render_template("excog1.html")


@app.route('/word', methods = ['post', 'get'])
def excog2():
    form = FlaskForm()
    global cogdomain
    global end
    if request.method == "POST":
        session["wordf"] = request.form.get("wordf")
        session["words"] = request.form.get("words")
        if int(session["wordf"])>=2 and int(session["words"])>=2:
            end=True
            cogdomain=1
            return diagnose("end")
        else:
            return redirect(url_for("excog3"))
    return render_template("excog2.html")


@app.route('/focus', methods = ['post', 'get'])
def excog3():
    form = FlaskForm()
    global end
    global cogdomain
    if request.method == "POST":
        session["focusf"] = request.form.get("focusf")
        session["focuss"] = request.form.get("focuss")
        if int(session["focusf"])>=2 and int(session["focuss"])>=2:
            end = True
            cogdomain=1
            return diagnose("end")
        else:
            end = True
            cogdomain=0
            return diagnose("end")

    return render_template("excog3.html")

@app.route('/end', methods = ['post', 'get'])
def end():
    form = FlaskForm()
    if request.method=="POST":
        return redirect(url_for('home'))
    #return render_template("example4.html")

    if end:
        fatiguedata = ((int(session["fatiguescoref"]) + int(session['fatiguescores']))/2)
        minexdata = ((int(session["minexf"]) + int(session['minexs']))/2)
        sleepdata = ((int(session["sleepf"]) + int(session['sleeps'])) / 2)
        cogdata = ((int(session["rememberf"]) + int(session['remembers']))/2)
        #data = [fatiguedata, minexdata, sleepdata, cogdata]
        data = np.array([[fatiguedata, minexdata, sleepdata, cogdata]])
        result = randomForest.rf2.predict(data)
        if result[0] == 1:
            return f"The random forest model predicts ME/CFS. Model accuracy is {randomForest.accuracy}"
        else:
            return f"The random forest model does not predict ME/CFS. Model accuracy is {randomForest.accuracy}"

        #return f"{result}"


if __name__ == '__main__':
    app.run(debug=True)
