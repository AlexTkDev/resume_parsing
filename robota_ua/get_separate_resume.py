"""Export individual resumes from robota.ua using Selenium."""

import argparse
import logging
import os
from urllib.parse import urlparse
from typing import Any

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from core.logging_config import setup_logging
from core.utils import get_user_data_from_file, save_to_txt
from core.selenium import setup_selenium, teardown_selenium

from parsers.robota_ua import parse_robota_ua_resume

logger = logging.getLogger(__name__)


def get_separate_resume(driver: Any, url: str) -> tuple[str, str]:
    """Extract resume details from a URL."""
    try:
        driver.get(url)
    except WebDriverException as exc:
        logger.error("Failed to open %s: %s", url, exc)
        return "", "No courses, trainings, or certificates provided."

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "alliance-shared-ui-prof-resume-experience")
            )
        )
        return parse_robota_ua_resume(driver.page_source)
    except TimeoutException as exc:
        logger.error("Error extracting data from %s: %s", url, exc)
        return "", "No courses, trainings, or certificates provided."


def main(file: str) -> None:
    """Main entry point for exporting individual resumes."""
    driver = setup_selenium()

    try:
        user_data = get_user_data_from_file(file)

        if not user_data:
            logger.warning("No user data found in the file.")
            return

        output_dir = "ready-made_resumes"
        os.makedirs(output_dir, exist_ok=True)

        for data in user_data:
            link = data["link"]
            logger.info("Processing page: %s", link)
            resume, courses = get_separate_resume(driver, link)

            user_id = urlparse(link).path.rstrip("/").split("/")[-1] or "unknown"
            filename = os.path.join(output_dir, f"resume_{user_id}.txt")

            resume_text = f"{resume}\n\nCourses, trainings, certificates:\n{courses}"
            save_to_txt(resume_text, filename)
            logger.debug("Saved resume %s", user_id)
    finally:
        teardown_selenium(driver)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export separate resume files from robota.ua.")
    parser.add_argument("--file", type=str, required=True, help="JSON file with candidate data")
    args = parser.parse_args()

    setup_logging()
    main(args.file)