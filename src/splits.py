# local
from segment import Segment


class Splits:

    def __init__(self, splits_xml_root):
        segments_xml_root = splits_xml_root.find('Segments')
        self.segments = map(lambda segment_xml_root: Segment(segment_xml_root), segments_xml_root)

    def get_segment_summaries(self, min_attempt_id=None, comparison='GameTime', zscore_cutoff=None):
        return map(lambda segment: segment.get_summary(min_attempt_id=min_attempt_id,
                                                       comparison=comparison,
                                                       zscore_cutoff=zscore_cutoff),
                   self.segments)
