import requests
from models.db_models import Quote


def get_quotes(order_by='created_on', descending=True):
    if descending:
        q = Quote.query.order_by(getattr(Quote, order_by).desc()).all()
    else:
        q = Quote.query.order_by(getattr(Quote, order_by)).all()
    return q


def getRandQuote():
	r = requests.get('https://api.quotable.io/quotes/random/?limit=5')
	if r:
		return r.json()
	else:
		return {"content": "None", "author":"None"}
