import argparse
import os
import json
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By

from html_stream_parser import parse_resume_page


def setup_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def get_user_data(file):
    """Extract candidate links and names from a JSON file."""
    user_data = []
    if not os.path.exists(file) or os.path.getsize(file) == 0:
        print(f"No data found in {file}.")
        return user_data

    try:
        with open(file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        print(f"Invalid JSON in {file}.")
        return user_data

    if not isinstance(data, list):
        print(f"{file} must contain a JSON list.")
        return user_data

    for item in data:
        if (
            isinstance(item, dict)
            and item.get('link')
            and item['link'] != 'No link'
            and item.get('name')
        ):
            user_data.append({
                'link': item['link'],
                'name': item['name']
            })
    return user_data


def get_separate_resume(driver, url):
    """Extract resume details from a URL."""
    try:
        driver.get(url)
    except WebDriverException as exc:
        print(f"Failed to open {url}: {exc}")
        return "", "No courses, trainings, or certificates provided."

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'alliance-shared-ui-prof-resume-experience'))
        )

        return parse_resume_page(driver.page_source)
    except TimeoutException as e:
        print(f"Error extracting data from {url}: {e}")
        return "", "No courses, trainings, or certificates provided."


def save_to_txt(resume_data, courses_data, filename):
    """Save extracted resume data as a text file."""
    with open(filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(f"{resume_data}\n\nCourses, trainings, certificates:\n{courses_data}")


def main(file):
    driver = setup_selenium()
    try:
        user_data = get_user_data(file)

        if not user_data:
            print("No user data found in the file.")
            return

        output_dir = 'ready-made_resumes'
        os.makedirs(output_dir, exist_ok=True)

        for data in user_data:
            link = data['link']
            print(f'Processing page: {link}')
            resume, courses = get_separate_resume(driver, link)

            user_id = urlparse(link).path.rstrip('/').split('/')[-1] or "unknown"

            filename = os.path.join(output_dir, f'resume_{user_id}.txt')
            save_to_txt(resume, courses, filename)
    finally:
        driver.quit()


if __name__ == "__main__":
    # python robota_ua/get_separate_resume.py --file resumes_robota_ua.json
    parser = argparse.ArgumentParser(description="Export separate resume files.")
    parser.add_argument('--file', type=str, required=True,
                        help='JSON file with candidate data')
    args = parser.parse_args()
    main(args.file)
