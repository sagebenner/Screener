from flask import Blueprint, render_template, session, request, redirect, url_for

screener_views = Blueprint('screener_views', __name__)

@screener_views.route('/home', methods=['post', 'get'])
def home():
    session["pagenum"] = 0
    survey = 'classic'
    if request.method == "POST":
        session["pagenum"] += 1
        return redirect(url_for("page1"))
    return render_template("home.html", session=session)



