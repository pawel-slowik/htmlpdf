"""tests for render_html"""

# pylint: disable=missing-docstring

from htmlpdf import render_html

def test_simple() -> None:
    yaml_inputs = ["foo:\n  bar"]
    template = "{{foo}}"
    assert render_html(yaml_inputs, template) == "bar"

def test_overwrite() -> None:
    yaml_inputs = ["foo:\n  bar", "foo:\n  baz"]
    template = "{{foo}}"
    assert render_html(yaml_inputs, template) == "baz"

def test_reuse() -> None:
    yaml_inputs = ["foo: &alias\n  bar", "hello: *alias"]
    template = "{{foo}} {{hello}}"
    assert render_html(yaml_inputs, template) == "bar bar"

def test_tags() -> None:
    yaml_inputs = ["foo:\n  _bar_ __baz__"]
    template = "{{foo}}"
    assert render_html(yaml_inputs, template) == "<em>bar</em> <strong>baz</strong>"
