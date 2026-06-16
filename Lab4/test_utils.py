# test_utils.py
import pytest
from utils import clamp, merge_sorted, parse_pair, unique_sorted

# === Teste pentru CLAMP ===
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


# === Teste pentru MERGE_SORTED ===
def test_merge_sorted_normal():
    assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]

def test_merge_sorted_one_empty():
    assert merge_sorted([], [1, 2, 3]) == [1, 2, 3]
    assert merge_sorted([1, 2, 3], []) == [1, 2, 3]

def test_merge_sorted_both_empty():
    assert merge_sorted([], []) == []

def test_merge_sorted_duplicates():
    assert merge_sorted([1, 2, 2], [2, 3, 4]) == [1, 2, 2, 2, 3, 4]


# === Teste pentru PARSE_PAIR ===
def test_parse_pair_valid():
    assert parse_pair("10:20") == (10, 20)
    assert parse_pair("-1:5") == (-1, 5)

def test_parse_pair_no_separator():
    with pytest.raises(ValueError):
        parse_pair("hello")

def test_parse_pair_too_many_separators():
    with pytest.raises(ValueError):
        parse_pair("1:2:3")

def test_parse_pair_invalid_ints():
    with pytest.raises(ValueError):
        parse_pair("abc:123")


# === Teste pentru UNIQUE_SORTED (Prinderea bug-ului) ===
def test_unique_sorted_normal():
    # Pe asta s-ar putea să treacă
    assert unique_sorted([2, 1, 2]) == [1, 2]

def test_unique_sorted_bug_trigger():
    # Trei sau mai multe duplicate consecutive vor pica testul din cauza indicelui sărit
    assert unique_sorted([1, 1, 1, 2]) == [1, 2]


#==============================================
from hypothesis import given, assume
from hypothesis import strategies as st

# Proprietăți pentru clamp
@given(st.integers(), st.integers(), st.integers())
def test_clamp_properties(x, lo, hi):
    assume(lo <= hi)
    result = clamp(x, lo, hi)
    
    # Proprietatea 1: Rezultatul e mereu între lo și hi
    assert lo <= result <= hi
    
    # Proprietatea 2: Idempotență
    assert clamp(result, lo, hi) == result
    
    # Proprietatea 3: No-op dacă e deja în range
    if lo <= x <= hi:
        assert result == x

# Proprietăți pentru merge_sorted
sorted_lists = st.lists(st.integers()).map(sorted)

@given(sorted_lists, sorted_lists)
def test_merge_sorted_properties(a, b):
    result = merge_sorted(a, b)
    
    # Proprietatea 1: Rezultatul este sortat
    assert result == sorted(result)
    
    # Proprietatea 2: Lungimea este suma lungimilor
    assert len(result) == len(a) + len(b)
    
    # Proprietatea 3: Este o permutare a concatenării (conține exact aceleași elemente)
    assert sorted(result) == sorted(a + b)