import requests
from flask import abort
from datetime import datetime
import pytz
from models.db_models import Quote


# Get quotes from the databases.
def get_quotes(page, order_by='created_on', descending=True):
    try:
        if descending:
            q = Quote.query.order_by(getattr(Quote, order_by).desc()).paginate(page=page, per_page=5)
        else:
            q = Quote.query.order_by(getattr(Quote, order_by)).paginate(page=page, per_page=5)
        return q
    except Exception as e:
        abort(500, description="Database couldn't be reached.")

# Query the database for random quotes from an external API
def getRandQuote():
    try:
        r = requests.get('https://api.quotable.io/quotes/random/?limit=4')
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        abort(400, description="Couldn't reach external server, probably check your internet or try again later.!")
      

# Format the date to get elapsed time
def format_post_date(post_date, timezone='UTC'):
    current_datetime_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    post_date_utc = post_date.replace(tzinfo=pytz.timezone(timezone))

    time_difference = current_datetime_utc - post_date_utc

    # If the post is within the same day, display hours or minutes ago
    if time_difference.days == 0:
        seconds = time_difference.seconds

        if seconds < 60:
            return f"{seconds}sec ago"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}min ago"
        else:
            hours = seconds // 3600
            if hours == 1:
                return f"{hours}hr ago"
            return f"{hours}hrs ago"
    else:
        # If the post is from a different day, display day and month
        return post_date.strftime("%b %d")


