def merge(splits, args):
    print('Merging on "{}"'.format(args.merge_point))
    segments = list(splits.segments)
    merge_segment_match = [(index, seg) for (index, seg) in enumerate(segments) if seg.name == args.merge_point]
    if len(merge_segment_match) != 1:
        print('Expected to find 1 matching segment, found {} instead'.format(len(merge_segment_match)))
        return
    (merge_segment_index, merge_segment) = merge_segment_match[0]
    next_segment = segments[merge_segment_index + 1]
    print('Merging into "{}"'.format(next_segment.name))
    print('Remaining functionality: TODO')
