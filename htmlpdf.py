#!/usr/bin/env python3
"""A tool for creating PDF documents from YAML data and Jinja2 HTML templates."""

import re
import collections.abc
import os.path
import logging
import numbers
from xml.etree import ElementTree
from typing import Mapping, Iterable, Callable, Union
import yaml
import jinja2
import weasyprint
from cssselect2 import ElementWrapper
from unidecode import unidecode

Leaf = Union[str, numbers.Real, None]
Node = Union[Mapping, Iterable, Leaf]

def create_pdf(html: str, base_url: str, output_filename: str) -> None:
    """Create a PDF file from an HTML document."""
    font_config = weasyprint.fonts.FontConfiguration()
    document = weasyprint.HTML(string=html, base_url=base_url)
    document.write_pdf(target=output_filename, font_config=font_config)

def render_html_files(data_filenames: Iterable[str], html_template_filename: str) -> str:
    """Render a Jinja2 template using YAML files as data sources.

    Data from any subsequent YAML file overwrites data loaded from previous
    file(s). You can refer to nodes from previous files using YAML anchors and
    aliases: https://yaml.org/spec/1.2/spec.html#alias// """
    return render_html(
        (open(df, "r").read() for df in data_filenames),
        open(html_template_filename, "r").read()
    )

def render_html(yaml_inputs: Iterable[str], html_template: str) -> str:
    """Render a Jinja2 template using YAML strings as data sources."""
    return jinja2.Template(html_template).render(
        recursive_map(
            yaml.safe_load("\n".join(yaml_inputs)),
            process_tags
        )
    )

def process_tags(inp: Leaf) -> Leaf:
    """Process a limited subset of Markdown into HTML."""
    if isinstance(inp, numbers.Real):
        return inp
    if inp is None:
        return inp
    tags = [
        (r"__([^_]+)__", r"<strong>\1</strong>"),
        (r"_([^_]+)_", r"<em>\1</em>"),
    ]
    for pattern, replacement in tags:
        inp = re.sub(pattern, replacement, inp)
    return inp

def recursive_map(node: Node, func: Callable[[Leaf], Leaf]) -> Node:
    """Apply a function recursively to a node (similar to map(), but recursive)."""
    if isinstance(node, str):
        return func(node)
    if isinstance(node, numbers.Real):
        return func(node)
    if node is None:
        return func(node)
    if isinstance(node, collections.abc.Mapping):
        return {k: recursive_map(v, func) for k, v in node.items()}
    if isinstance(node, collections.abc.Iterable):
        return [recursive_map(elem, func) for elem in node]
    raise ValueError

def get_title(html: str) -> str:
    """Extract the meta title from an HTML document."""
    wrapper = ElementWrapper.from_html_root(ElementTree.fromstring(html))
    meta: Mapping[str, str] = weasyprint.html.get_html_metadata(wrapper, "")
    return meta["title"]

def create_output_filename(title: str) -> str:
    """Create a CLI friendly filename (no spaces, no accented characters etc.)"""
    ascii_title: str = unidecode(title)
    return re.sub(r"\W+", "_", ascii_title) + ".pdf"

def get_base_url(filename: str) -> str:
    """Get a base URL that is usable as WeasyPrint base_url parameter."""
    dirname = os.path.dirname(filename)
    return dirname if dirname else "."

def enable_weasyprint_logging() -> None:
    """Make the WeasyPrint warnings visible.

    Most HTML / CSS errors are not fatal and will not prevent WeasyPrint from
    rendering a document, but they can make the document appear ugly or broken.
    Therefore it's important to take heed of the warning messages.
    https://weasyprint.readthedocs.io/en/latest/tutorial.html#logging"""
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("WeasyPrint %(levelname)s: %(message)s"))
    weasyprint.LOGGER.addHandler(handler)

def main() -> None:
    """A simple CLI for the module. Run with `-h` for help."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", action="append", dest="data_filenames", required=True,
        help="YAML data filename (repeat to load multiple files)", metavar="DATA_FILENAME",
    )
    parser.add_argument(
        "-t", dest="html_template_filename", required=True,
        help="HTML template filename"
    )
    parser.add_argument(
        "-o", dest="output_filename", required=False,
        help="output PDF filename (default: generated based on HTML document title)"
    )
    args = parser.parse_args()
    enable_weasyprint_logging()
    html = render_html_files(args.data_filenames, args.html_template_filename)
    output_filename = (
        args.output_filename
        if args.output_filename
        else create_output_filename(get_title(html))
    )
    create_pdf(html, get_base_url(args.html_template_filename), output_filename)
    print("output saved to %s" % output_filename)

if __name__ == "__main__":
    main()
