import unittest
from unittest.mock import patch, MagicMock
from selenium.common.exceptions import WebDriverException
import scrape

class TestScrapeWebsite(unittest.TestCase):

    @patch('scrape.webdriver.Chrome')
    @patch('scrape.time.sleep')
    def test_scrape_website_success(self, mock_sleep, mock_chrome):
        # Setup mock
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_driver.page_source = "<html><body>Test Content</body></html>"

        # Call function
        result = scrape.scrape_website("https://example.com")

        # Asserts
        self.assertEqual(result, "<html><body>Test Content</body></html>")
        mock_chrome.assert_called_once()
        mock_driver.get.assert_called_once_with("https://example.com")
        mock_driver.quit.assert_called_once()

    @patch('scrape.webdriver.Chrome')
    @patch('scrape.time.sleep')
    def test_scrape_website_adds_https(self, mock_sleep, mock_chrome):
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_driver.page_source = "<html><body>Test Content</body></html>"

        result = scrape.scrape_website("example.com")

        self.assertEqual(result, "<html><body>Test Content</body></html>")
        mock_driver.get.assert_called_once_with("https://example.com")

    def test_scrape_website_empty_url(self):
        with self.assertRaisesRegex(ValueError, "Empty or invalid URL provided"):
            scrape.scrape_website("")

        with self.assertRaisesRegex(ValueError, "Empty or invalid URL provided"):
            scrape.scrape_website("   ")

        with self.assertRaisesRegex(ValueError, "Empty or invalid URL provided"):
            scrape.scrape_website(None)

    @patch('scrape.webdriver.Chrome')
    def test_scrape_website_chrome_exception(self, mock_chrome):
        mock_chrome.side_effect = WebDriverException("Test Exception")

        with self.assertRaisesRegex(RuntimeError, "ChromeDriver failed to start"):
            scrape.scrape_website("https://example.com")

    @patch('scrape.webdriver.Chrome')
    def test_scrape_website_quits_on_exception_during_get(self, mock_chrome):
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_driver.get.side_effect = Exception("Some get exception")

        with self.assertRaisesRegex(Exception, "Some get exception"):
            scrape.scrape_website("https://example.com")

        mock_driver.quit.assert_called_once()

    @patch('scrape.time.sleep')
    @patch('scrape.webdriver.Chrome')
    def test_scrape_website_sleeps(self, mock_chrome, mock_sleep):
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_driver.page_source = "<html><body>Test Content</body></html>"

        scrape.scrape_website("https://example.com")
        mock_sleep.assert_called_once_with(2)

if __name__ == '__main__':
    unittest.main()
