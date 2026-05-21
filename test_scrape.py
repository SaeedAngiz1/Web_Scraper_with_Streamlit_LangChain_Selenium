import unittest
from scrape import extract_body_content

class TestScrape(unittest.TestCase):
    def test_extract_body_content_simple(self):
        html = "<html><head><title>Test</title></head><body><p>Hello World</p></body></html>"
        expected = "<body><p>Hello World</p></body>"
        self.assertEqual(extract_body_content(html), expected)

    def test_extract_body_content_with_attributes(self):
        html = "<html><head></head><body class='main' id='content'><p>Text</p></body></html>"
        expected = "<body class=\"main\" id=\"content\"><p>Text</p></body>"
        self.assertEqual(extract_body_content(html), expected)

    def test_extract_body_content_no_body(self):
        html = "<html><head><title>Test</title></head></html>"
        expected = ""
        self.assertEqual(extract_body_content(html), expected)

    def test_extract_body_content_empty_string(self):
        html = ""
        expected = ""
        self.assertEqual(extract_body_content(html), expected)

    def test_extract_body_content_malformed_html(self):
        html = "<body><p>Unclosed body tag"
        expected = "<body><p>Unclosed body tag</p></body>"
        self.assertEqual(extract_body_content(html), expected)

if __name__ == '__main__':
    unittest.main()
