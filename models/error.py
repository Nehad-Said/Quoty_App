from flask import render_template
from models import app, db


# Handle 404 not found error with an html page.
@app.errorhandler(404)
def not_found(error):
	return render_template('not_found.html', error=error), 404

# Handle 500 not found error with an html page.
@app.errorhandler(500)
def not_found(error):
	if db.session.is_active:
		db.session.rollback()
	return render_template('server_error.html', error=error), 500