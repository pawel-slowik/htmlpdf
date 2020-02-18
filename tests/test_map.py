"""tests for recursive_map"""

# pylint: disable=missing-docstring

import pytest

from htmlpdf import recursive_map

def example_function(element):
    return set([element])

def test_int() -> None:
    assert recursive_map(5, example_function) == example_function(5)

def test_float() -> None:
    assert recursive_map(5.5, example_function) == example_function(5.5)

def test_str() -> None:
    assert recursive_map("test", example_function) == example_function("test")

def test_none() -> None:
    assert recursive_map(None, example_function) == example_function(None)

def test_list() -> None:
    assert recursive_map(["foo"], example_function) == [example_function("foo")]

def test_dict() -> None:
    assert recursive_map({"asd": "qwe"}, example_function) == {"asd": example_function("qwe")}

def test_recursive() -> None:
    start = [
        {"foo": ["bar"]}
    ]
    expected = [
        {"foo": [example_function("bar")]}
    ]
    assert recursive_map(start, example_function) == expected

def test_unhandled() -> None:
    with pytest.raises(ValueError):
        recursive_map(object, example_function)
