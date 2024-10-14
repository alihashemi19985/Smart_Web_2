from flask import Flask, redirect, render_template, Blueprint

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

