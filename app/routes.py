from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    Blueprint,
    session,
    request,
)
from flask_bcrypt import Bcrypt
from .database import User, db, Prediction, bcrypt
from .forms import RegistrationForm, LoginForm, InputForm
from  .model.model import prediction

bp = Blueprint("main", __name__)
# bcrypt = Bcrypt()


@bp.route("/")
def home():
    return render_template("home.html")


@bp.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("You already have an account. Please log in.", "warning")
            return redirect(url_for("main.login"))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Register Successfull')
        return redirect(url_for('main.login'))
    return render_template("register.html", form = form)

@bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_check = User.query.filter_by(username=username).first()
        if user_check is None:
            flash("This username is not registered. Please Register.", "warning")
            return redirect(url_for("main.login"))
        if user_check and bcrypt.check_password_hash(user_check.password, password):
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('main.input_data'))
        else:
            flash("Login failed. Please check your username and password.", "danger")
            return redirect(url_for("main.login"))
    return render_template("login.html", form=form)

def login_required(f):
    def wrap(*args, **kwargs):
        if "username" not in session:
            flash("You need to login first!", "danger")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


@bp.route("/input", methods=["GET", "POST"])
@login_required
def input_data():
    form=InputForm()

    if request.method == 'POST' and form.validate_on_submit():
        Pclass= form.Pclass.data
        sex = form.sex.data
        age= form.age.data
        embarked= form.embarked.data
    
        features = [Pclass, sex, age, embarked]
        predicted_class = prediction(features)  ##machine learning model
        user_check = User.query.filter_by(username =session['username']).first()
        new_input = Prediction(
            user_id= user_check.id,
            Pclass = Pclass,
            sex= sex,
            age= age,
            embarked = embarked,
            result = predicted_class
        )
        db.session.add(new_input)
        db.session.commit()
        return render_template("result.html" , predicted_class = predicted_class)
       
    return render_template("input.html", form = form)

@bp.route("/history", methods=["GET"])
@login_required
def history():
    current_user = User.query.filter_by(username=session["username"]).first()
    predictions = Prediction.query.filter_by(user_id=current_user.id).all()

    return render_template("history.html", predictions=predictions)
    

@bp.route("/error", methods=["GET"])
def error():
    
    return render_template("error.html")


@bp.route("/logout")
def logout():
    session.pop("username",None)
    session.clear()
    flash("You are logged out", "success")

    return redirect(url_for("main.home"))
