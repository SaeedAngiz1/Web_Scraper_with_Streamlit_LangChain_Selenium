import pytest
from streamlit.testing.v1 import AppTest
from unittest.mock import patch

@patch("parse.parse_content", side_effect=Exception("Mocked error"))
def test_parse_content_error(mock_parse):
    at = AppTest.from_file("main.py")

    # Set the state necessary to show the parsing section
    at.session_state["dom_content"] = "<html>Test content</html>"
    at.run()

    # Fill in the parse description
    at.text_area[0].set_value("extract prices")

    # Click the "Parse Content" button
    at.button[1].click().run()

    # Check that the error is displayed
    assert len(at.error) > 0

    # The error message should contain the exception details
    assert any("Mocked error" in e.value for e in at.error)
