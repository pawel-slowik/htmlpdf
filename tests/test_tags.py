"""tests for tag processing"""

# pylint: disable=missing-docstring,line-too-long

import pytest
from htmlpdf import Node, process_tags, process_tags_for_scalar


def test_no_tags() -> None:
    assert process_tags_for_scalar("No tags") == "No tags"


def test_no_matched_tag() -> None:
    assert process_tags_for_scalar("no _matched tag") == "no _matched tag"


def test_strong_tags() -> None:
    assert process_tags_for_scalar("__foo__ bar __baz__") == "<strong>foo</strong> bar <strong>baz</strong>"


def test_em_tags() -> None:
    assert process_tags_for_scalar("_foo_ bar _baz_") == "<em>foo</em> bar <em>baz</em>"


def test_mixed_tags() -> None:
    assert process_tags_for_scalar("__foo__ bar _baz_") == "<strong>foo</strong> bar <em>baz</em>"


def test_passthrough_none() -> None:
    assert process_tags_for_scalar(None) is None


def test_passthrough_int() -> None:
    assert process_tags_for_scalar(1) == 1


def test_passthrough_float() -> None:
    assert process_tags_for_scalar(0.1) == 0.1


@pytest.mark.parametrize(
    "input_node,expected_node",
    [
        pytest.param(
            [None, -0.5, 5, "x __y__ z"],
            [None, -0.5, 5, "x <strong>y</strong> z"],
            id="iterable",
        ),
        pytest.param(
            [[["_hola_"]]],
            [[["<em>hola</em>"]]],
            id="nested iterable",
        ),
        pytest.param(
            {-1: None, "2": -0.5, "three": 5, "": "x __y__ z"},
            {-1: None, "2": -0.5, "three": 5, "": "x <strong>y</strong> z"},
            id="mapping",
        ),
        pytest.param(
            {"a": {"b": {"c": "_d_"}}},
            {"a": {"b": {"c": "<em>d</em>"}}},
            id="nested mapping",
        ),
        pytest.param(
            {"x __y__ z": "x __y__ z"},
            {"x __y__ z": "x <strong>y</strong> z"},
            id="mapping does not modify key",
        ),
        pytest.param(
            {"iterable": ["_foo_"], "mapping": {"x": "_y_"}},
            {"iterable": ["<em>foo</em>"], "mapping": {"x": "<em>y</em>"}},
            id="mixed mapping and iterable",
        ),
    ]
)
def test_process_tags(input_node: Node, expected_node: Node) -> None:
    assert process_tags(input_node) == expected_node
