from constants.base import constants
from datetime import datetime

def get_date() -> str:
    """Get the current date in YYYY-MM-DD format.
    """
    today = datetime.now()
    day = today.strftime("%d")
    month = today.strftime("%m")
    year = today.strftime("%Y")
    today_format = f"{day}-{month}-{year}"
    return today_format

def get_day(date: (str | None)=None) -> str:
    """Get the day of date.

    Parameters
    -----------
        date (str): Date to get the day. It's optional. For default is the current date.
    """
    if date is None: date = get_date()
    day = date.split('-')[0]
    return day


def get_month(date: (str | None)=None) -> str:
    """Get the month of date.

    Parameters
    -----------
        date (str): Date to get the month. It's optional. For default is the current date.
    """
    if date is None: date = get_date()
    month = date.split('-')[1]
    return month

def get_year(date: (str | None)=None) -> str: 
    """Get the year of date.

    Parameters
    -----------
        date (str): Date to get the year. It's optional. For default is the current date.
    """
    if date is None: date = get_date()
    year = date.split('-')[2]
    return year

def get_month_to_clean(date: (str | None)=None) -> str:
    """Get the number of month to data delete.

    Parameters
    -----------
        date (str): Date to count down. It's optional. For default is the current date.
    """
    if date is None: date = get_date()
    month = int(date.split('-')[1])
    month -= constants.MONTHS_TO_KEEP + 1
    if month < 1: month += 12
    month = "0" + str(month) if month < 10 else str(month)
    return month

def verifyMonth(date_a: str, date_b: str) -> bool:
    """Verify if two date are in the same month.

    Parameters
    -----------
        date_a (str): First date.
        date_b (str): Second date.
    """
    month_a = int(date_a.split('-')[1])
    month_b = int(date_b.split('-')[1])
    return month_a == month_b