# lib
import math
import statistics

# local
import timeutil


def getSegmentsRoot(root):
    return root.find('Segments')


def getSegmentName(segment):
    return segment.find('Name').text


def getAttemptId(time):
    return int(time.attrib['id'])


def getGoldTime(segment, comparison='GameTime'):
    searchKey = 'BestSegmentTime/{}'.format(comparison)
    goldString = segment.find(searchKey).text
    timeTuple = timeutil.parseTime(goldString)
    return timeTuple


def getTimeIterMs(segment, minAttemptId=None, comparison='GameTime'):
    times = segment.findall('SegmentHistory/Time')
    if (type(minAttemptId) is int):
        times = filter(lambda x: getAttemptId(x) > minAttemptId, times)
    gameTimesRaw = map(lambda x: x.find(comparison), times)
    gameTimeElements = filter(lambda x: x is not None, gameTimesRaw)
    gameTimesText = map(lambda x: x.text, gameTimeElements)
    parsedTimes = map(timeutil.parseTime, gameTimesText)
    return map(timeutil.toMilliseconds, parsedTimes)


def getStats(segment, minAttemptId=None, comparison='GameTime'):
    times = list(getTimeIterMs(segment, minAttemptId, comparison))
    mean = int(statistics.mean(times))
    median = int(statistics.median(times))
    deviation = int(statistics.stdev(times))
    mean, median, deviation = removeOutliers(times, mean, deviation)
    gold = timeutil.toMilliseconds(getGoldTime(segment))
    return mean, deviation, getSegmentName(segment), median, gold


def deviationKey(stats):
    _, deviation, _, _, _ = stats
    return deviation


def getDeviationSorted(segments, minAttemptId=None, comparison='GameTime'):
    stats = map(lambda x: getStats(x, minAttemptId, comparison), segments)
    return sorted(stats, reverse=True, key=deviationKey)


def removeOutliers(times, mean, deviation):  # Calc Z Score and remove if outlier
    n = 0
    while n in range(len(times)):
        if ((times[n] - mean) / deviation > 3):  # Equation for Z Score
            times.pop(n)
        else:
            n += 1

    return (int(statistics.mean(times)), int(statistics.median(times)), int(statistics.stdev(times)))
