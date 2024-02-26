import requests
from datetime import datetime
import pytz
from models.db_models import Quote


def get_quotes(page, order_by='created_on', descending=True):
    if descending:
        q = Quote.query.order_by(getattr(Quote, order_by).desc()).paginate(page=page, per_page=7)
    else:
        q = Quote.query.order_by(getattr(Quote, order_by)).paginate(page=page, per_page=7)
    return q


def getRandQuote():
	r = requests.get('https://api.quotable.io/quotes/random/?limit=5')
	if r:
		return r.json()
	else:
		return {"content": "None", "author":"None"}
      

def format_post_date(post_date, timezone='UTC'):
    current_datetime_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    post_date_utc = post_date.replace(tzinfo=pytz.timezone(timezone))

    time_difference = current_datetime_utc - post_date_utc

    # If the post is within the same day, display hours or minutes ago
    if time_difference.days == 0:
        seconds = time_difference.seconds

        if seconds < 60:
            return f"{seconds} seconds ago"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} minutes ago"
        else:
            hours = seconds // 3600
            return f"{hours} hours ago"
    else:
        # If the post is from a different day, display day and month
        return post_date.strftime("%b %d")


