# local
from segment import Segment


def deviation_key(stats):
    _, deviation, _, _, _ = stats
    return deviation


class Splits:

    def __init__(self, splits_xml_root):
        self.__segments_xml_root__ = splits_xml_root.find('Segments')

    def get_deviations(self, min_attempt_id=None, comparison='GameTime'):
        segments = map(lambda segment_xml_root: Segment(segment_xml_root, comparison), self.__segments_xml_root__)
        stats = map(lambda segment: segment.get_stats(min_attempt_id=min_attempt_id), segments)
        return sorted(stats, reverse=True, key=deviation_key)
