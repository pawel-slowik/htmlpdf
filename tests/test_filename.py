"""tests for create_output_filename"""

# pylint: disable=missing-docstring

import string
import re

from htmlpdf import create_output_filename


def test_letters() -> None:
    assert create_output_filename(string.ascii_letters) == string.ascii_letters + ".pdf"


def test_numbers() -> None:
    assert create_output_filename(string.digits) == string.digits + ".pdf"


def test_space() -> None:
    assert create_output_filename(" ") == "_.pdf"


def test_punctuation() -> None:
    assert re.search(r"^_+\.pdf$", create_output_filename(string.punctuation))


def test_lowercase_accents() -> None:
    assert create_output_filename("ęóąśłżźćń") == "eoaslzzcn.pdf"


def test_uppercase_accents() -> None:
    assert create_output_filename("ĘÓĄŚŁŻŹĆŃ") == "EOASLZZCN.pdf"
