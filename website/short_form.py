from flask import Blueprint, render_template, session, request, redirect, url_for
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.utils
import numpy as np

short_form = Blueprint('short_form', __name__)


message = "Please enter a response for both frequency and severity before continuing"

@short_form.route('/soreness', methods=['post', 'get'])
def expem1():
    global pemname
    if request.method == "POST":
        soref = request.form.get("soref")
        sores = request.form.get("sores")
        if soref is not None and sores is not None:
            session["soref"] = soref
            session["sores"] = sores
            session['pagenum'] += 1

            if int(session["soref"]) >= 0 and int(session["sores"]) >= 0:
                session['pemscoref'] = session['soref']
                session['pemscores'] = session['sores']
                session['pemscore'] = (int(session['soref']) + int(session['sores'])) / 2
                pemname = 'soreness15'

                return redirect(url_for("short_form.excog1"))


        else:
            return render_template("expem1.html", pagenum=session['pagenum'], message=message)
    return render_template("expem1.html", pagenum=session['pagenum'], message='')

@short_form.route('/attention', methods=['post', 'get'])
def excog1():
    global cogname
    if request.method == "POST":
        attentionf = request.form.get("attentionf")
        attentions = request.form.get("attentions")
        if attentions is not None and attentionf is not None:
            session["attentionf"] = attentionf
            session["attentions"] = attentions
            session['pagenum'] += 1
            if int(session["attentionf"]) >= 0 and int(session["attentions"]) >= 0:
                session['cogscoref'] = int(attentionf)
                session['cogscores'] = int(attentions)
                cogname = 'difficulty37'
                session['cogscore'] = (int(session['attentionf']) + int(session['attentions'])) / 2
                end = True
                return redirect(url_for("short_form.musclepain"))
        else:
            return render_template("excog1.html", message=message, pagenum=session['pagenum'])
    return render_template("excog1.html", message='', pagenum=session['pagenum'])

@short_form.route('/musclepain', methods=['post', 'get'])
def musclepain():
    global end
    if request.method == "POST":
        musclef = request.form.get("musclef")
        mucles = request.form.get("muscles")
        if musclef is not None and mucles is not None:
            session["musclef"] = musclef
            session["muscles"] = mucles
            session['pagenum'] += 1
            return redirect(url_for("short_form.bloating"))
        else:
            return render_template("musclepain.html", message=message, pagenum=session['pagenum'])
    return render_template("musclepain.html", message='', pagenum=session['pagenum'])

@short_form.route('/bloating', methods=['post', 'get'])
def bloating():
    global end
    if request.method == "POST":
        bloatf = request.form.get("bloatf")
        bloats = request.form.get("bloats")
        if bloats is not None and bloatf is not None:
            session["bloatf"] = bloatf
            session["bloats"] = bloats
            session['pagenum'] += 1
            return redirect(url_for("short_form.bowel"))
        else:
            return render_template("bloating.html", message=message, pagenum=session['pagenum'])
    return render_template("bloating.html", message='', pagenum=session['pagenum'])

@short_form.route('/bowel', methods=['post', 'get'])
def bowel():
    global end
    if request.method == "POST":
        bowelf = request.form.get("bowelf")
        bowels = request.form.get("bowels")
        if bowels is not None and bowelf is not None:
            session["bowelf"] = bowelf
            session["bowels"] = bowels
            session['pagenum'] += 1
            return redirect(url_for("short_form.unsteady"))
        else:
            return render_template("bowel.html", message=message, pagenum=session['pagenum'])
    return render_template("bowel.html", message='', pagenum=session['pagenum'])


@short_form.route('/unsteady', methods=['post', 'get'])
def unsteady():
    global end
    if request.method == "POST":
        unsteadyf = request.form.get("unsteadyf")
        unsteadys = request.form.get("unsteadys")
        if unsteadyf is not None and unsteadys is not None:
            session["unsteadyf"] = unsteadyf
            session["unsteadys"] = unsteadys
            session['pagenum'] += 1
            return redirect(url_for("short_form.cold_limbs"))
        else:
            return render_template("unsteady.html", message=message, pagenum=session['pagenum'])
    return render_template("unsteady.html", message='', pagenum=session['pagenum'])

@short_form.route('/cold_limbs', methods=['post', 'get'])
def cold_limbs():
    global end
    if request.method == "POST":
        limbsf = request.form.get("limbsf")
        limbss = request.form.get("limbss")
        if limbsf is not None and limbss is not None:
            session["limbsf"] = limbsf
            session["limbss"] = limbss
            session['pagenum'] += 1
            return redirect(url_for("short_form.hot_cold"))
        else:
            return render_template("limbs.html", message=message, pagenum=session['pagenum'])
    return render_template("limbs.html", message='', pagenum=session['pagenum'])

@short_form.route('/hot_cold', methods=['post', 'get'])
def hot_cold():
    global end
    if request.method == "POST":
        hotf  = request.form.get("hotf")
        hots = request.form.get("hots")
        if hotf is not None and hots is not None:
            session["hotf"] = hotf
            session["hots"] = hots
            session['pagenum'] += 1
            return redirect(url_for("short_form.flu"))
        else:
            return render_template("hot.html", message=message, pagenum=session['pagenum'])
    return render_template("hot.html", message='', pagenum=session['pagenum'])

@short_form.route('/flu', methods=['post', 'get'])
def flu():
    global end
    if request.method == "POST":
        fluf  = request.form.get("fluf")
        flus = request.form.get("flus")
        if fluf is not None and flus is not None:
            session["fluf"] = fluf
            session["flus"] = flus
            session['pagenum'] += 1
            return redirect(url_for("short_form.smells"))
        else:
            return render_template("flu.html", message=message, pagenum=session['pagenum'])
    return render_template("flu.html", message='', pagenum=session['pagenum'])

@short_form.route('/smells', methods=['post', 'get'])
def smells():
    global end
    global survey
    if request.method == "POST":
        smellf = request.form.get("smellf")
        smells = request.form.get("smells")
        if smellf is not None and smells is not None:
            session["smellf"] = smellf
            session["smells"] = smells
            session['pagenum'] += 1
            survey='rf14'
            return redirect(url_for('short_form.reduction'))
        else:
            return render_template("smells.html", message=message, pagenum=session['pagenum'])
    return render_template("smells.html", message='', pagenum=session['pagenum'])

@short_form.route('/reduction', methods=['post', 'get'])
def reduction():
    msg_reduction = "Please select one of the options before continuing"
    if request.method == 'POST':
        reduction = request.form.get('reduction')
        if reduction is not None:
            session['reduction'] = reduction
            session['pagenum'] += 1
            return redirect(url_for('short_form.graph2'))
        else:
            return render_template("reduction.html", message=msg_reduction, pagenum=session['pagenum'])
    return render_template('reduction.html', message='', pagenum=session['pagenum'])


@short_form.route('/short_form_dx', methods=['post', 'get'])
def graph2():
    import domainScores as ds

    fatiguescore = (int(session["fatiguescoref"]) + int(session["fatiguescores"])) / 2
    pemscore = (int(session["minexf"]) + int(session["minexs"]) + int(session['soref']) + int(session['sores'])) / 4
    sleepscore = (int(session["sleepf"]) + int(session["sleeps"])) / 2
    cogscore = (int(session["rememberf"]) + int(session["remembers"]) + int(session['attentionf']) +
                int(session['attentions'])) / 4
    painscore = (int(session['musclef']) + int(session['muscles'])) / 2
    gastroscore = (int(session['bloatf']) + int(session['bloats']) + int(session['bowelf']) +
                   int(session['bowels'])) / 4
    orthoscore = (int(session['unsteadyf']) + int(session['unsteadys'])) / 2
    circscore = (int(session['limbsf']) + int(session['limbss']) + int(session['hotf']) + int(session['hots'])) / 4
    immunescore = (int(session['fluf']) + int(session['flus'])) / 2
    neuroenscore = (int(session['smellf']) + int(session['smells'])) / 2

    user_scores = [fatiguescore, pemscore, sleepscore, cogscore, painscore, gastroscore, orthoscore, circscore,
                   immunescore, neuroenscore]

    shortform_items = ['fatigue13c', 'soreness15c', 'minimum17c', 'unrefreshed19c',
                       'musclepain25c', 'bloating29c', 'remember36c', 'difficulty37c',
                       'bowel46c', 'unsteady48c', 'limbs56c', 'hot58c', 'flu65c',
                       'smells66c']

    df = ds.sdf

    mecfs = df[(df['dx'] == 1)]
    controls = df[(df['dx'] != 1)]


    cfsdomains = np.mean(mecfs.iloc[:, 110:120], axis=0)

    # This assesses the IOM Criteria
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
    if (int(session['minexf']) >= 2 and int(session['minexs'] >= 2) or (
            int(session['soref']) >= 2 and int(session['sores']) >= 2)):
        iompemcheck = "Yes"
    if int(session['sleepf']) >= 2 and int(session['sleeps']) >= 2:
        iomsleepcheck = "Yes"
    if (int(session['rememberf']) and int(session['remembers']) >= 2 ) or (
            int(session['attentionf']) >= 2 and int(session['attentions']) >= 2):
        iomcogcheck = "Yes"

    if iomfatiguecheck == "Yes" and iomreductioncheck == "Yes" and iompemcheck == "Yes" and iomsleepcheck == "Yes" and iomcogcheck == "Yes":
        iom_msg = "Your answers indicate you may meet the IOM Criteria for ME/CFS. To compare your" \
                  " scores with more case definitions, continue to the next section"
        iomdxcheck = "Met"

    else:
        iom_msg = 'Your responses do not meet the IOM Criteria for ME/CFS. To assess more case definitions, ' \
                  'continue to the next section'
        iomdxcheck = "Not met"

    if iomfatiguecheck == "Yes" or iompemcheck == "Yes" or iomsleepcheck == "Yes" or iomcogcheck == "Yes":
        screen_message = "Your scores meet a threshold of 2 or greater on frequency and severity of least one major symptom. " \
                         "We recommend continuing to the next section (DSQ-Short Form) for more in-depth assessment."
    else:
        screen_message = "Your scores do not meet a threshold of 2 frequency or severity for any of the major symptoms." \
                         "It is unlikely that you have ME/CFS based on your self-report scores."

    # This assesses the Canadian Consensus Criteria, one of the three major case definitions we use

    ccc_dx = False

    if int(session['fatiguescoref']) >= 2 and int(session['fatiguescores']) >= 2:
        ccc_fatigue = 1

        ccc_fatiguecheck = "Yes"
    else:
        ccc_fatigue = 0
        ccc_fatiguecheck = "No"
    if int(session['reduction']) == 1:
        ccc_reduction = "Yes"
    else:
        ccc_reduction = "No"
    if int(session['musclef']) >= 2 and int(session['muscles']) >= 2:
        ccc_pain = 1
        ccc_paincheck = "Yes"
    else:
        ccc_pain = 0
        ccc_paincheck = "No"
    if int(session['sleepf']) >= 2 and int(session['sleeps']) >= 2:
        ccc_sleep = 1
        ccc_sleepcheck = "Yes"
    else:
        ccc_sleep = 0
        ccc_sleepcheck = "No"
    if (int(session['minexf']) >= 2 and int(session['minexs']) >= 2) or (
            int(session['soref']) >= 2 and int(session['sores']) >= 2):
        ccc_pem = 1
        ccc_pemcheck = "Yes"
    else:
        ccc_pem = 0
        ccc_pemcheck = "No"
    if (int(session['rememberf']) >= 2 and int(session['remembers']) >= 2) or (
            int(session['attentionf']) >= 2 and int(session['attentions']) >= 2):
        ccc_cog = 1
        ccc_cogcheck = "Yes"
    else:
        ccc_cog = 0
        ccc_cogcheck = "No"

    if (int(session['unsteadyf']) >= 2 and int(session['unsteadys']) >= 2) or (
            int(session['bowelf']) >= 2 and int(session['bowels']) >= 2) or (
            int(session['bloatf']) >= 2 and int(session['bloats']) >= 2):
        ccc_auto = 1
        ccc_autocheck = "Yes"
    else:
        ccc_auto = 0
        ccc_autocheck = "No"
    if (int(session['limbsf']) >= 2 and int(session['limbss']) >= 2) or (
            int(session['hotf']) >= 2 and int(session['hots']) >= 2):
        ccc_neuro = 1
        ccc_neurocheck = "Yes"
    else:
        ccc_neuro = 0
        ccc_neurocheck = "No"
    if (int(session['fluf']) >= 2 and int(session['flus']) >= 2) or (
            int(session['smellf']) >= 2 and int(session['smells']) >= 2):
        ccc_immune = 1
        ccc_immunecheck = "Yes"
    else:
        ccc_immune = 0
        ccc_immunecheck = "No"
    ccc_poly = np.sum([ccc_auto, ccc_neuro, ccc_immune])
    # most of the symptoms are required, but there is one polythetic criteria, shown here by ccc_poly
    if np.sum([ccc_fatigue, ccc_pem, ccc_sleep, ccc_pain, ccc_cog]) >= 5 and ccc_poly >= 2:
        ccc_dx = "Met"
        ccc_msg = "Your responses suggest that you meet the Canadian Consensus Criteria for ME/CFS. " \
                  "To compare your symptoms with more case definitions, click Continue."
    else:
        ccc_dx = "Not met"
        ccc_msg = "Your responses do not meet the Canadian Consensus Criteria for ME/CFS. " \
                  "To compare your symptoms with more case definitions, click Continue."

    # categories = [*feature_list, feature_list[0]]
    categories = ['Fatigue', 'PEM', 'Sleep', 'Cognitive Impairment', 'Pain', 'Gastro Problems',
                  'Orthostatic Intolerance', 'Circulatory Problems', 'Immune System', 'Neuroendocrine Problems']
    print(categories)


    # Creates a figure using the plotly library, which can be dynamically embedded in the HTML page
    fig = go.Figure(
        data=[
            go.Bar(y=user_scores, x=categories, name="Your scores"),
            go.Bar(y=cfsdomains, x=categories,
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

    # This converts to figure fig to a JSON object so it can be dynamically rendered with javascript on the page
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("graph2.html", graphJSON=graphJSON, ccc_msg=ccc_msg, ccc_fatiguecheck=ccc_fatiguecheck,
                           ccc_pemcheck=ccc_pemcheck, ccc_paincheck=ccc_paincheck, ccc_sleepcheck=ccc_sleepcheck,
                           ccc_cogcheck=ccc_cogcheck, ccc_autocheck=ccc_autocheck, ccc_immunecheck=ccc_immunecheck,
                           ccc_neurocheck=ccc_neurocheck, ccc_dx=ccc_dx, ccc_reduction=ccc_reduction,
                           iomfatiguecheck=iomfatiguecheck, iomreductioncheck=iomreductioncheck,
                           iompemcheck=iompemcheck, iomdxcheck=iomdxcheck, iom_msg=iom_msg,
                           iomsleepcheck=iomsleepcheck, iomcogcheck=iomcogcheck
                           )