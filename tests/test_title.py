"""tests for get_title"""

# pylint: disable=missing-docstring

from htmlpdf import get_title


def test_letters() -> None:
    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>Lorem ipsum</title>
</head>
<body>
</body>
</html>
"""
    assert get_title(html) == "Lorem ipsum"
