import datetime

def get_date() -> str:
    """Return the yesterday date in the format YYYY-MM-DD"""
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")