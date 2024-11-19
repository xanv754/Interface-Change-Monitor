import datetime

def get_date() -> str:
    """Return the current date in the format YYYY-MM-DD"""
    # day = datetime.datetime.now().day - 1
    day = datetime.datetime.now().day
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    return f'{year}-{month}-{day}'