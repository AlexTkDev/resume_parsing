"""Fetch resume listings from robota.ua using Selenium."""

import argparse
import logging
from typing import Any

from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from core.logging_config import setup_logging
from core.utils import save_to_json
from core.selenium import setup_selenium, teardown_selenium
from core.http import rate_limit

from parsers.robota_ua import parse_robota_ua_listings

logger = logging.getLogger(__name__)


def fetch_resumes(url: str, driver: Any) -> list[dict[str, Any]]:
    """Fetch and parse resume listings from a URL using Selenium."""
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section.cv-card"))
        )
    except (TimeoutException, WebDriverException) as exc:
        logger.error("Failed to load resumes from %s: %s", url, exc)
        return []

    return parse_robota_ua_listings(driver.page_source)


def main(pages: int, skill: str | None = None) -> None:
    """Main entry point for fetching resume listings."""
    driver = setup_selenium()

    try:
        if skill:
            base_url = f"https://robota.ua/candidates/{skill}/ukraine"
        else:
            base_url = "https://robota.ua/candidates/all/ukraine"

        for page in tqdm(range(1, pages + 1), desc="Processing pages"):
            url = f"{base_url}?page={page}"
            logger.info("Processing page %d: %s", page, url)

            rate_limit()

            resumes = fetch_resumes(url, driver)
            logger.info("Found %d resumes on page %d.", len(resumes), page)

            if not resumes:
                logger.warning("No resumes found on page %d. Stopping.", page)
                break

            save_to_json(resumes, "resumes_robota_ua.json")
            logger.info("Saved %d resumes from page %d", len(resumes), page)
    finally:
        teardown_selenium(driver)

    logger.info("Data saved to resumes_robota_ua.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse resume listings from robota.ua.")
    parser.add_argument("--pages", type=int, default=2, help="Number of pages to process (default: 2)")
    parser.add_argument("--skill", type=str, default=None, help="Search keyword, for example 'python'")
    args = parser.parse_args()

    setup_logging()
    main(args.pages, args.skill)