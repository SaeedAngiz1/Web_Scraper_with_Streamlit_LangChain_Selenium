import pytest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest

@patch('scrape.scrape_website')
def test_scrape_website_error(mock_scrape):
    """Test that a scraping error is properly caught and displayed in the UI."""
    mock_scrape.side_effect = Exception("Simulated connection error")

    at = AppTest.from_file("main.py").run()

    # Enter URL
    at.text_input[0].input("http://example.com").run()

    # Click Scrape Site button
    for btn in at.button:
        if btn.label == "Scrape Site":
            btn.click().run()
            break

    # Check if error is displayed
    assert len(at.error) > 0, "Expected an error message to be displayed"
    assert "Simulated connection error" in at.error[0].value
