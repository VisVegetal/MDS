import pytest
from hypothesis import given
from hypothesis import strategies as st
from merge_sorted import merge_sorted

def test_merge_sorted_normal():
    assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]

def test_merge_sorted_one_empty():
    assert merge_sorted([], [1, 2, 3]) == [1, 2, 3]
    assert merge_sorted([1, 2, 3], []) == [1, 2, 3]

def test_merge_sorted_both_empty():
    assert merge_sorted([], []) == []

def test_merge_sorted_duplicates():
    assert merge_sorted([1, 2, 2], [2, 3, 4]) == [1, 2, 2, 2, 3, 4]

sorted_lists = st.lists(st.integers()).map(sorted)

@given(sorted_lists, sorted_lists)
def test_merge_sorted_properties(a, b):
    result = merge_sorted(a, b)
    assert result == sorted(result)
    assert len(result) == len(a) + len(b)
    assert sorted(result) == sorted(a + b)
