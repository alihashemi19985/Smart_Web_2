
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    Blueprint,
    session,
    request,
)
bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    return render_template("home.html")


@bp.route("/register", methods=["POST", "GET"])
def register():
    # code here
    return render_template("register.html")

@bp.route("/login", methods=["POST", "GET"])
def login():
    #code here
    return render_template("login.html")

@bp.route("/input", methods=["GET", "POST"])
def input_data():
    
    return render_template("input.html")
@bp.route("/result", methods=["GET", "POST"])
def result():
    
    return render_template("result.html")

@bp.route("/history", methods=["GET"])
def history():
    
    return render_template("history.html")

@bp.route("/logout")
def logout():
    session.pop("username",None)
    session.clear()
    flash("You are logged out", "success")

    return redirect(url_for("main.index"))