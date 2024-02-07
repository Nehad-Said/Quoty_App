"""
    Module for the tweets routes
"""

from flask import render_template, url_for, flash, redirect, send_from_directory
from models import app, db, bcrypt
from models.form import RegistrationForm, LoginForm
from models.db_models import User, Tweet
from flask_login import login_user, current_user, logout_user

quotes = [
    {
        'content': "People's effort is directly proportional to value",
        'author': 'abdul',
        'created_on': '2023-04-12'
    },
    {
        'content': "You walk the way you're broken",
        'author': 'moha',
        'created_on': '2023-10-20'
    },
    {
        'content': "Two heads are better than one",
        'author': 'alex',
        'created_on': '2022-06-22'
    },
    {
        'content': "Love is like a song, it gets boring with time, can't be played forever and plays for a specific time",
        'author': 'ALX',
        'created_on': '2020-11-10'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", quotes=quotes)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        pw_hsh = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=pw_hsh)
        db.session.add(user)
        db.session.commit()
        flash(f"Account for {form.username.data} successfully created", 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/login", methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid Credentials, Please try again.!", 'danger')
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)
