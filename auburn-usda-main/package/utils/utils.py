import time


def formatEpochTimeToDuration(seconds: float):
    """Formats epoch time as hh:mm:ss to represent duration.
    For example, 13:43:20 represents 13 hours, 43 minutes, and 20 seconds

    :param seconds: epoch time
    """
    return time.strftime("%H:%M:%S", time.gmtime(seconds))


def formatEpochTimeToClockTime(seconds: float):
    """Formats epoch time as mm/dd hh:mm to represent clock time.
    For example, 09-12 21:00 PST represents September 12th at 9:00PM PST.
    Timezones include daylight savings time.
    
    :param seconds: epoch time
    """
    return time.strftime("%m/%d %H:%M", time.localtime(seconds)) + " " + time.tzname[time.localtime().tm_isdst]
