"""Fetch resume listings from work.ua."""

import argparse
import logging
from typing import Any

from tqdm import tqdm

from core.logging_config import setup_logging
from core.utils import save_to_json
from core.http import fetch_with_retry, rate_limit

from parsers.work_ua import parse_work_ua_listings

logger = logging.getLogger(__name__)


def fetch_resumes(url: str) -> list[dict[str, Any]]:
    """Fetch and parse resume listings from a URL."""
    html = fetch_with_retry(url)
    if html is None:
        return []
    return parse_work_ua_listings(html)


def main(pages: int, skill: str | None = None) -> None:
    """Main entry point for fetching resume listings."""
    if skill:
        base_url = f"https://www.work.ua/resumes-{skill}/"
    else:
        base_url = "https://www.work.ua/resumes/?ss=1"

    for page in tqdm(range(1, pages + 1), desc="Processing pages"):
        separator = "&" if "?" in base_url else "?"
        url = f"{base_url}{separator}page={page}"
        logger.info("Processing page %d: %s", page, url)

        rate_limit()

        resumes = fetch_resumes(url)

        if not resumes:
            logger.warning("No resumes found on page %d. Stopping.", page)
            break

        save_to_json(resumes, "resumes_work_ua.json")
        logger.info("Saved %d resumes from page %d", len(resumes), page)

    logger.info("Data saved to resumes_work_ua.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse resume listings from work.ua.")
    parser.add_argument("--pages", type=int, default=5, help="Number of pages to process (default: 5)")
    parser.add_argument("--skill", type=str, default=None, help="Search keyword, for example 'python'")
    args = parser.parse_args()

    setup_logging()
    main(args.pages, args.skill)