# intervals.py

def merge_intervals(intervals):
    """Merge overlapping or adjacent intervals.
    merge_intervals([(1, 3), (2, 5), (8, 10)]) -> [(1, 5), (8, 10)]
    merge_intervals([(1, 5), (2, 3)])           -> [(1, 5)]
    Each interval is (start, end) with start <= end.
    """
    if not intervals:
        return []

    # Sortăm intervalele după punctul de start
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]

    for current in sorted_intervals[1:]:
        prev_start, prev_end = merged[-1]
        curr_start, curr_end = current

        # Dacă intervalul curent se suprapune sau este adiacent cu cel precedent
        if curr_start <= prev_end:
            # Modificăm capătul superior al ultimului interval salvat
            merged[-1] = (prev_start, max(prev_end, curr_end))
        else:
            merged.append(current)

    return merged