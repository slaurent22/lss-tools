from typing import Iterable
from xml.etree.ElementTree import Element as XMLElement
from .segment import Segment, SegmentSummary


class Splits:
    segments: Iterable[Segment]

    def __init__(self, splits_xml_root: XMLElement):
        #We need last_attempt and attempts to adjust min_attempt_id
        #in case the ls attempt counter is not accurate
        segments_xml_root = splits_xml_root.find('Segments')
        attempts_xml_root = splits_xml_root.find('AttemptHistory')
        last_attempt = attempts_xml_root.findall('Attempt')[-1].get('id')
        attempts = splits_xml_root.find('AttemptCount').text
        assert segments_xml_root is not None
        self.segments = map(lambda segment_xml_root: Segment(segment_xml_root, attempts, last_attempt), segments_xml_root)

    def get_segment_summaries(self,
                              min_attempt_id=None,
                              comparison='GameTime',
                              zscore_cutoff=None,
                              last_runs=None) -> Iterable[SegmentSummary]:
        return map(lambda segment: segment.get_summary(min_attempt_id=min_attempt_id,
                                                       comparison=comparison,
                                                       zscore_cutoff=zscore_cutoff,
                                                       last_runs=last_runs),
                   self.segments)
