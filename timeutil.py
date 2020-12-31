from datetime import datetime
import math

MS_PER_SECOND = 1000
MS_PER_MINUTE = 60 * MS_PER_SECOND
MS_PER_HOUR = 60 * MS_PER_MINUTE
MICROSENDS_PER_MILLLISECOND = 1000

def qrem(a, b):
    return a // b, a % b

def parseTime(timeText):
    parsed = datetime.strptime(timeText[0:len(timeText)-2], "%H:%M:%S.%f")
    return parsed.hour, parsed.minute, parsed.second, int(parsed.microsecond / MICROSENDS_PER_MILLLISECOND)

def toMilliseconds(timeTuple):
    hour, minute, second, millisecond = timeTuple
    return hour * MS_PER_HOUR + minute * MS_PER_MINUTE + second * MS_PER_SECOND + millisecond

def fromMilliseconds(microseconds):
    ms_left = microseconds
    hour,   ms_left = qrem(ms_left, MS_PER_HOUR)
    minute, ms_left = qrem(ms_left, MS_PER_MINUTE)
    second, ms_left = qrem(ms_left, MS_PER_SECOND)
    return hour, minute, second, ms_left

def formatTimeTuple(timeTuple):
    hour, minute, second, millisecond = timeTuple
    # datetime.strftime("%H:%M:%S.%f")
    return "{:02d}:{:02d}:{:02d}.{:03d}".format(hour, minute, second, millisecond)
