import argparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")


def get_data_by_selenium(url: str) -> str:
    """Load a page with Selenium and return its HTML."""
    service = ChromeService(ChromeDriverManager().install())
    with webdriver.Chrome(service=service, options=chrome_options) as driver:
        driver.get(url)
        print(f"Page loaded: {driver.title}")
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            data = driver.page_source
        except Exception as e:
            print(f"Error: {e}")
            data = driver.page_source
    return data


def save_html_to_file(html_content: str, file_path: str):
    """Save HTML content to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)


def main(url: str, output: str):
    html_data = get_data_by_selenium(url)
    save_html_to_file(html_data, output)
    print(f"HTML saved to '{output}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save a rendered HTML page.")
    parser.add_argument("url", help="Page URL to load")
    parser.add_argument(
        "--output",
        default="page_content.html",
        help="Output HTML file path (default: page_content.html)",
    )
    args = parser.parse_args()
    main(args.url, args.output)
