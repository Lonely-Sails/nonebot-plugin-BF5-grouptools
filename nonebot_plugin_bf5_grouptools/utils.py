from datetime import timedelta, datetime


def format_time(utc: str):
    utc_time = datetime.strptime(utc, '%Y-%m-%dT%H:%M:%S.%fZ')
    beijing_time = utc_time + timedelta(hours=8)
    return beijing_time.strftime('%Y-%m-%dT%H:%M:%S')
