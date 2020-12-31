# lib
import math
import statistics

# local
import timeutil

config = {
    'comparison': 'GameTime'
}

def getSegmentsRoot(root):
    return root.find('Segments')

def getSegmentName(segment):
    return segment.find('Name').text

def getAttemptId(time):
    return int(time.attrib['id'])

def getGoldTime(segment):
    searchKey = 'BestSegmentTime/{}'.format(config['comparison'])
    goldString = segment.find(searchKey).text
    timeTuple = timeutil.parseTime(goldString)
    return timeTuple

def getTimeIterMs(segment, minAttemptId=None):
    times = segment.findall('SegmentHistory/Time')
    if (type(minAttemptId) is int):
        times = filter(lambda x: getAttemptId(x) > minAttemptId, times)
    gameTimesRaw = map(lambda x: x.find(config['comparison']), times)
    gameTimeElements = filter(lambda x: x is not None, gameTimesRaw)
    gameTimesText = map(lambda x: x.text, gameTimeElements)
    parsedTimes = map(timeutil.parseTime, gameTimesText)
    return map(timeutil.toMilliseconds, parsedTimes)

def getStats(segment, minAttemptId=None):
    times = list(getTimeIterMs(segment, minAttemptId=minAttemptId))
    mean = int(statistics.mean(times))
    variance = int(statistics.variance(times))
    return mean, variance, getSegmentName(segment)

def varianceKey(stats):
    _, variance, _ = stats
    return variance

def getVarianceSorted(segments, minAttemptId=None):
    stats = map(lambda x: getStats(x, minAttemptId), segments)
    return sorted(stats, reverse=True, key=varianceKey)
