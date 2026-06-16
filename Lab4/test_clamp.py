# test_clamp.py
import pytest
from hypothesis import given, assume
from hypothesis import strategies as st
from clamp import clamp

def test_clamp_inside_range():
    assert clamp(5, 1, 10) == 5

def test_clamp_outside_below():
    assert clamp(0, 1, 10) == 1

def test_clamp_outside_above():
    assert clamp(15, 1, 10) == 10

def test_clamp_exactly_boundaries():
    assert clamp(1, 1, 10) == 1
    assert clamp(10, 1, 10) == 10

def test_clamp_lo_equal_hi():
    assert clamp(5, 5, 5) == 5
    assert clamp(10, 5, 5) == 5

@given(st.integers(), st.integers(), st.integers())
def test_clamp_properties(x, lo, hi):
    assume(lo <= hi)
    result = clamp(x, lo, hi)
    assert lo <= result <= hi
    assert clamp(result, lo, hi) == result
    if lo <= x <= hi:
        assert result == x