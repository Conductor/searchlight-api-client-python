import datetime
import math

EPOCH = datetime.datetime.strptime("2009-07-26", "%Y-%m-%d")


def week_number(date):
    """Convert date of format YYYY-MM-DD to Searchlight Time Period Number"""
    try:
        return math.ceil((datetime.datetime.strptime(date, "%Y-%m-%d") - EPOCH).days / 7)
    except ValueError:
        raise ValueError("Date must match format YYYY-MM-DD")
