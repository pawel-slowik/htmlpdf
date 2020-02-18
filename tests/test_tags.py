"""tests for process_tags"""

# pylint: disable=missing-docstring

from htmlpdf import process_tags

def test_no_tags() -> None:
    assert process_tags("No tags") == "No tags"

def test_no_matched_tag() -> None:
    assert process_tags("no _matched tag") == "no _matched tag"

def test_strong_tags() -> None:
    assert process_tags("__foo__ bar __baz__") == "<strong>foo</strong> bar <strong>baz</strong>"

def test_em_tags() -> None:
    assert process_tags("_foo_ bar _baz_") == "<em>foo</em> bar <em>baz</em>"

def test_mixed_tags() -> None:
    assert process_tags("__foo__ bar _baz_") == "<strong>foo</strong> bar <em>baz</em>"
