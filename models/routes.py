"""
    Module for the tweets routes
"""

from flask import render_template, url_for, flash, redirect, send_from_directory, request
from models import app, db, bcrypt
from models.form import RegistrationForm, LoginForm, SubmitQuoteForm, EditQuoteForm
from models.db_models import User, Quote
from flask_login import login_user, current_user, logout_user, login_required


def get_quotes(order_by='created_on', descending=True):
    if descending:
        q = Quote.query.order_by(getattr(Quote, order_by).desc()).all()
    else:
        q = Quote.query.order_by(getattr(Quote, order_by)).all()
    return q



@app.route("/")
def index():
    quotes = get_quotes()
    return render_template("index.html", quotes=quotes)

@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    quotes = get_quotes()
    form = SubmitQuoteForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            user = current_user
            quote_content = form.content.data
            q = Quote(content=quote_content, author=user)
            db.session.add(q)
            db.session.commit()
            flash("Quote succesfully added", "success")
            return redirect(url_for('home'))
        
    return render_template("home.html", title="Home", form=form, quotes=quotes)


@app.route("/profile/<username>", methods=['GET', 'POST'])
@login_required
def profile(username):
    form = EditQuoteForm()
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('profile.html', user=user, form=form)

@app.route('/profile/<username>/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_q(username, id):
    quote = Quote.query.get(id)
    new_quote = request.form.get('edit_quote')

    # Update quote content in the database
    quote.content = new_quote
    db.session.commit()
    flash("Quote succesfully updated", "success")    

    return redirect(url_for('profile', username=username))


@app.route('/profile/<username>/del/<id>', methods=['GET', 'POST'])
@login_required
def del_q(username, id):
    quote = Quote.query.get(id)

    if quote:
        db.session.delete(quote)
        db.session.commit()
        flash("Quote deleted succesfully", "success")

    else:
        flash("Quote not found", "success")    

    return redirect(url_for('profile', username=username))


@app.route("/register", methods=('GET', 'POST'))
def register():
    quotes = get_quotes()
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
    return render_template("register.html", form=form, quotes=quotes)

@app.route("/login", methods=('GET', 'POST'))
def login():
    quotes = get_quotes()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome back {user.username}", 'success')
            return redirect(url_for('home'))
        else:
            flash("Invalid Credentials, Please try again.!", 'danger')
    return render_template("login.html", form=form, quotes=quotes)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)
