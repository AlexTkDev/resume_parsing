"""Export individual resumes from work.ua."""

import argparse
import logging
import os
from urllib.parse import urlparse

from core.logging_config import setup_logging
from core.utils import get_user_links_from_file, save_to_txt
from core.http import fetch_with_retry

from parsers.work_ua import parse_work_ua_resume

logger = logging.getLogger(__name__)


def get_separate_resume(url: str) -> str:
    """Fetch and parse a single resume from a URL."""
    html = fetch_with_retry(url)
    if html is None:
        logger.error("Failed to fetch resume from %s", url)
        return "No resume found."
    return parse_work_ua_resume(html)


def main(file: str) -> None:
    """Main entry point for exporting individual resumes."""
    links = get_user_links_from_file(file)
    if not links:
        logger.warning("No links found in the file.")
        return

    output_dir = "ready-made_resumes"
    os.makedirs(output_dir, exist_ok=True)

    for link in links:
        logger.info("Processing page: %s", link)
        resume = get_separate_resume(link)
        user_id = urlparse(link).path.rstrip("/").split("/")[-1] or "unknown"
        save_to_txt(resume, os.path.join(output_dir, f"resume_{user_id}.txt"))
        logger.debug("Saved resume %s", user_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export separate resume files from work.ua.")
    parser.add_argument("--file", type=str, required=True, help="JSON file with resume links")
    args = parser.parse_args()

    setup_logging()
    main(args.file)