"""Selenium setup and teardown utilities."""

import logging
import os
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


def setup_selenium(headless: Optional[bool] = None) -> webdriver.Chrome:
    """Set up and return a Selenium Chrome driver."""
    if headless is None:
        headless = os.getenv("HEADLESS", "true").lower() == "true"

    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    logger.debug("Selenium driver initialized (headless=%s)", headless)
    return driver


def teardown_selenium(driver: webdriver.Chrome) -> None:
    """Quit the Selenium driver."""
    driver.quit()
    logger.debug("Selenium driver closed")