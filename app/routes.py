from flask import Flask, redirect, render_template, Blueprint

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    return render_template("home.html")
