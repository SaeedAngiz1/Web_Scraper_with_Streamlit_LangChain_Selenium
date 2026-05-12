import time
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup


def scrape_website(website: str) -> str:
    print("Launching Chrome browser...")

    if not website or website.strip() == "":
        raise ValueError("Empty or invalid URL provided.")

    if not website.startswith(("http://", "https://")):
        website = "https://" + website
        print("DEBUG — corrected URL:", website)



    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(

            options=options,
        )
    except WebDriverException as e:
        raise RuntimeError(
            "ChromeDriver failed to start. "
            "Make sure Chrome is installed or chromedriver is in your PATH matches your Chrome version."
        ) from e

    try:
        driver.get(website)
        print("Page loaded successfully.")
        time.sleep(2)
        html = driver.page_source
    finally:
        driver.quit()

    return html


def extract_body_content(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content: str) -> str:
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip()
        for line in cleaned_content.splitlines()
        if line.strip()
    )
    return cleaned_content


def split_dom_content(dom_content: str, max_length: int = 6000) -> list[str]:
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]
