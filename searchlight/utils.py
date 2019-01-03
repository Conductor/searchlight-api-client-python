import datetime
import math


EPOCH = datetime.datetime.strptime("07-26-2009", "%m-%d-%Y")


def week_number(date):
    return math.ceil((datetime.datetime.strptime(date, "%m-%d-%Y") - EPOCH).days / 7)
