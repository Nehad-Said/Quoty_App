from flask import render_template
from models import app, db


@app.errorhandler(404)
def not_found(error):
	return render_template('not_found.html'), 404


@app.errorhandler(500)
def not_found(error):
	db.session.rollback()
	return render_template('server_error.html'), 500