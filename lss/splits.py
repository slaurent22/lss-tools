from typing import Iterable
from xml.etree.ElementTree import Element as XMLElement
from .segment import Segment, SegmentSummary


class Splits:
    segments: Iterable[Segment]

    def __init__(self, splits_xml_root: XMLElement):
        segments_xml_root = splits_xml_root.find('Segments')
        assert segments_xml_root is not None
        self.segments = map(lambda segment_xml_root: Segment(segment_xml_root), segments_xml_root)

    def get_segment_summaries(self,
                              min_attempt_id=None,
                              comparison='GameTime',
                              zscore_cutoff=None) -> Iterable[SegmentSummary]:
        return map(lambda segment: segment.get_summary(min_attempt_id=min_attempt_id,
                                                       comparison=comparison,
                                                       zscore_cutoff=zscore_cutoff),
                   self.segments)
