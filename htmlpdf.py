#!/usr/bin/env python3

import json
import re
import os.path
import logging
from xml.etree import ElementTree
from typing import Mapping
import jinja2
import weasyprint
from cssselect2 import ElementWrapper
from unidecode import unidecode

def create_pdf(html: str, base_url: str, output_filename: str) -> None:
    font_config = weasyprint.fonts.FontConfiguration()
    document = weasyprint.HTML(string=html, base_url=base_url)
    document.write_pdf(target=output_filename, font_config=font_config)

def render_html(data_filename: str, html_template_filename: str) -> str:
    data = json.load(open(data_filename, "r"))
    html_template = open(html_template_filename, "r").read()
    return jinja2.Template(html_template).render(data)

def get_title(html: str) -> str:
    wrapper = ElementWrapper.from_html_root(ElementTree.fromstring(html))
    meta: Mapping[str, str] = weasyprint.html.get_html_metadata(wrapper, "")
    return meta["title"]

def create_output_filename(title: str) -> str:
    ascii_title: str = unidecode(title)
    return re.sub(r"\W+", "_", ascii_title) + ".pdf"

def get_base_url(filename: str) -> str:
    dirname = os.path.dirname(filename)
    return dirname if dirname else "."

def enable_weasyprint_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("WeasyPrint %(levelname)s: %(message)s"))
    weasyprint.LOGGER.addHandler(handler)

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", dest="data_filename", required=True,
        help="data filename"
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
    html = render_html(args.data_filename, args.html_template_filename)
    output_filename = (
        args.output_filename
        if args.output_filename
        else create_output_filename(get_title(html))
    )
    create_pdf(html, get_base_url(args.html_template_filename), output_filename)
    print("output saved to %s" % output_filename)

if __name__ == "__main__":
    main()
