import datetime
import math

EPOCH = datetime.datetime.strptime("2009-07-26", "%Y-%m-%d")


def week_number(date):
<<<<<<< HEAD
    return int(math.ceil((datetime.datetime.strptime(date, "%m-%d-%Y") - EPOCH).days / 7))
=======
    """Convert date of format YYYY-MM-DD to Searchlight Time Period Number"""
    try:
        return math.ceil((datetime.datetime.strptime(date, "%Y-%m-%d") - EPOCH).days / 7)
    except ValueError:
        raise ValueError("Date must match format YYYY-MM-DD")
>>>>>>> 22e97ab66c15934b33471f31c1d974d1da65e438
