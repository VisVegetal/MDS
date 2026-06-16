# chunking.py

def chunk(lst, n):
    """Split lst into consecutive groups of n elements.
    The last group may be shorter.
    """
    if n <= 0:
        raise ValueError("n must be greater than 0")
        
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])
    return result

def flatten(lst_of_lsts):
    """Concatenate a list of lists into a single list."""
    result = []
    for sublist in lst_of_lsts:
        result.extend(sublist)
    return result