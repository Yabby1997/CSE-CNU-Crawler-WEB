from datetime import datetime
import pytz


def convert_time(endDateTime, mask, dateonly=False):
    if dateonly:
        return datetime.strptime(endDateTime, mask).strftime('%Y년 %m월 %d일')
    else:
        return datetime.strptime(endDateTime, mask).strftime('%Y-%m-%d-%H-%M')


def time_validation(endDateTime, mask, days):
    endDateTime = datetime.strptime(endDateTime, mask)
    endDateTime = endDateTime.replace(tzinfo=pytz.timezone('Asia/Seoul'))
    now = datetime.now(pytz.timezone('Asia/Seoul'))
    delta = int((now - endDateTime).days)
    return delta <= days
