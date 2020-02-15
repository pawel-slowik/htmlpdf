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
