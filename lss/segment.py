from typing import Any, Dict, Iterable, List, Tuple, TypedDict
import statistics
from xml.etree.ElementTree import Element as XMLElement
from .timeutil import parse_time, to_milliseconds, TimeTuple

def exists(it):
    return (it is not None)


def get_attempt_id(time_xml_node: XMLElement) -> int:
    return int(time_xml_node.attrib['id'])


def z_score(value: int, mean: int, deviation: int) -> float:
    return (value - mean) / deviation


def remove_outliers(times: List[int], mean: int, deviation: int, zscore_cutoff: int = 0) -> Tuple[int, int, int]:
    n = 0
    while n in range(len(times)):
        absolute_z_score = abs(z_score(times[n], mean, deviation))
        if (absolute_z_score > zscore_cutoff):
            times.pop(n)
        else:
            n += 1

    return (int(statistics.mean(times)), int(statistics.median(times)), int(statistics.stdev(times)))


class SegmentStats(TypedDict):
    mean: int
    median: int
    deviation: int


class SegmentSummary(TypedDict):
    name: str
    gold: int
    gold_zscore: float
    stats: SegmentStats


class Segment:
    name: str

    def __init__(self, xml_root: XMLElement, attempts: int, last_attempt: int):
        name_root = xml_root.find('Name')
        assert name_root is not None
        name_text = name_root.text
        assert name_text is not None
        self.name = name_text
        self.__xml_root__ = xml_root
        self.attempts = attempts
        self.last_attempt = last_attempt

    def get_gold_time(self, comparison='GameTime') -> int:
        search_key = 'BestSegmentTime/{}'.format(comparison)
        gold_root = self.__xml_root__.find(search_key)
        assert gold_root is not None
        gold_string = gold_root.text
        assert gold_string is not None
        time_tuple = parse_time(gold_string)
        return to_milliseconds(time_tuple)

    def get_game_time_elements(self, min_attempt_id=None, comparison='GameTime') -> Iterable[XMLElement]:
        times: List[XMLElement] = self.__xml_root__.findall('SegmentHistory/Time')
        if (type(min_attempt_id) is int):
            times = list(filter(lambda x: get_attempt_id(x) > min_attempt_id, times))

        game_time_elements_raw = map(lambda x: x.find(comparison), times)
        game_time_elements_not_none: Any = filter(exists, game_time_elements_raw)
        return game_time_elements_not_none

    def get_game_time_dict(self, min_attempt_id=None, comparison='GameTime') -> Dict[int, TimeTuple]:
        time_dict: Dict[int, TimeTuple] = {}
        times: List[XMLElement] = list(filter(exists, self.__xml_root__.findall('SegmentHistory/Time')))
        if (type(min_attempt_id) is int):
            times = list(filter(lambda x: get_attempt_id(x) > min_attempt_id, times))

        for time_xml_node in times:
            attempt_id = get_attempt_id(time_xml_node)
            time = time_xml_node.find(comparison)
            if (not exists(time)):
                continue
            assert time is not None
            time_text = time.text
            assert time_text is not None
            time_tuple = parse_time(time_text)
            time_dict[attempt_id] = time_tuple
        return time_dict

    def get_time_iter_ms(self, min_attempt_id=None, last_runs=None, comparison='GameTime') -> Iterable[int]:
        # the Any types annotation is here because I can't figure out how to turn Iterable[Optional[XMLElement]]
        # into Iterable[XMLElement] to make the mypy type checker happy
        if(last_runs is not None):
            min_attempt_id = int(self.last_attempt) - last_runs
        elif(min_attempt_id is not None):  #adjusts min_attempt_id in case ls counter is not accurate
            temp = int(self.attempts) - min_attempt_id
            min_attempt_id = int(self.last_attempt) - temp
        
        game_time_elements: Any = self.get_game_time_elements(min_attempt_id, comparison)
        game_times_text: Iterable[str] = map(lambda x: x.text, game_time_elements)
        parsed_times = map(parse_time, game_times_text)
        return map(to_milliseconds, parsed_times)

    def get_summary(self, min_attempt_id=None, comparison='GameTime', zscore_cutoff=None, last_runs=None) -> SegmentSummary:
        times = list(self.get_time_iter_ms(comparison=comparison, min_attempt_id=min_attempt_id, last_runs=last_runs))
        mean = int(statistics.mean(times))
        median = int(statistics.median(times))
        deviation = int(statistics.stdev(times))
        if type(zscore_cutoff) is int:
            mean, median, deviation = remove_outliers(times, mean, deviation, zscore_cutoff=zscore_cutoff)
        stats: SegmentStats = {
            'mean': mean,
            'median': median,
            'deviation': deviation
        }

        gold = self.get_gold_time(comparison=comparison)
        gold_zscore = round(z_score(gold, mean, deviation), 2)
        return {
            'name': self.name,
            'gold': gold,
            'gold_zscore': gold_zscore,
            'stats': stats
        }
    
