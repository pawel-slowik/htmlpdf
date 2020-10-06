[![Build Status][build-badge]][build-url]
[![Coverage][coverage-badge]][coverage-url]

[build-badge]: https://travis-ci.org/pawel-slowik/htmlpdf.svg?branch=master
[build-url]: https://travis-ci.org/pawel-slowik/htmlpdf
[coverage-badge]: https://codecov.io/gh/pawel-slowik/htmlpdf/branch/master/graph/badge.svg
[coverage-url]: https://codecov.io/gh/pawel-slowik/htmlpdf

A tool for creating PDF documents from YAML data and [Jinja2][jinja2] HTML
templates. Uses the excellent [WeasyPrint][weasyprint] library for rendering
HTML to PDF.

[jinja2]: https://palletsprojects.com/p/jinja/
[weasyprint]: https://weasyprint.org/

## Installation

The script is not packaged, run it from a repository clone. Install
dependencies with:

	pip3 install -r requirements.txt

## Usage

Run:

	./htmlpdf.py -i input.yaml -t template.html -o output.pdf

## Examples

	cd examples
	../htmlpdf.py -i CV_PL.yaml -t CV_PL.html -o CV_PL.pdf
	../htmlpdf.py -i CV_PL.yaml -i CV_star_ratings.yaml -t CV_star_ratings.html -o CV_star_ratings.pdf
