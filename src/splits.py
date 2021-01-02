# local
from segment import Segment


def get_segments_xml_root(root):
    return root.find('Segments')


def deviation_key(stats):
    _, deviation, _, _, _ = stats
    return deviation


def get_deviations(segments_xml_root, minAttemptId=None, comparison='GameTime'):
    segments = map(lambda xml_root: Segment(xml_root, comparison), segments_xml_root)
    stats = map(lambda x: x.get_stats(min_attempt_id=minAttemptId), segments)
    return sorted(stats, reverse=True, key=deviation_key)
