from datetime import datetime
from datetime import timedelta
import time


def get_localtime_str():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


def get_backdate_str(num_of_days, date_format="%Y-%m-%d %H:%M:%S"):
    return (datetime.now() - timedelta(num_of_days)).strftime(date_format)


def get_local_timestamp():
    return str(time.time())

