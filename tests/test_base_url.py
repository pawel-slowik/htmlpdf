"""tests for get_base_url"""

# pylint: disable=missing-docstring

from htmlpdf import get_base_url

def test_single_level() -> None:
    assert get_base_url("foo/bar.css") == "foo"

def test_multiple_levels() -> None:
    assert get_base_url("foo/bar/baz.css") == "foo/bar"

def test_current_directory() -> None:
    assert get_base_url("bar.css") == "."
