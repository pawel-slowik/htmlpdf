"""tests for tag processing"""

# pylint: disable=missing-docstring

import pytest
from htmlpdf import Leaf, Node, process_tags, process_tags_for_scalar


@pytest.mark.parametrize(
    "input_leaf,expected_output",
    [
        pytest.param(
            "No tags",
            "No tags",
            id="plain text",
        ),
        pytest.param(
            "no _matched tag",
            "no _matched tag",
            id="unmatched tag",
        ),
        pytest.param(
            "__foo__ bar __baz__",
            "<strong>foo</strong> bar <strong>baz</strong>",
            id="strong tags",
        ),
        pytest.param(
            "_foo_ bar _baz_",
            "<em>foo</em> bar <em>baz</em>",
            id="em tags",
        ),
        pytest.param(
            "__foo__ bar _baz_",
            "<strong>foo</strong> bar <em>baz</em>",
            id="mixed tags",
        ),
        pytest.param(
            "foo [example ??](https://www.example.com) bar",
            'foo <a href="https://www.example.com">example ??</a> bar',
            id="link",
        ),
        pytest.param(
            None,
            None,
            id="passthrough None",
        ),
        pytest.param(
            1,
            1,
            id="passthrough int",
        ),
        pytest.param(
            0.1,
            0.1,
            id="passthrough float",
        ),
    ]
)
def test_process_tags_for_scalar(input_leaf: Leaf, expected_output: Leaf) -> None:
    assert process_tags_for_scalar(input_leaf) == expected_output


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
