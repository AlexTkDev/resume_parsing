import argparse
import os
import json
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from tqdm import tqdm

from html_stream_parser import parse_resume_listings


def setup_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def load_json_list(filename):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return []

    try:
        with open(filename, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        print(f"Warning: {filename} is not valid JSON. Starting with an empty list.")
        return []

    if not isinstance(data, list):
        print(f"Warning: {filename} must contain a JSON list. Starting with an empty list.")
        return []

    return data


def fetch_resumes(url, driver):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'section.cv-card'))
        )
    except (TimeoutException, WebDriverException) as exc:
        print(f"Failed to load resumes from {url}: {exc}")
        return []

    return parse_resume_listings(driver.page_source)


def save_to_json(data, filename):
    existing_data = load_json_list(filename)
    unique_resumes = {}

    for item in existing_data + data:
        link = item.get('link') if isinstance(item, dict) else None
        if link and link != 'No link':
            unique_resumes[link] = item

    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(list(unique_resumes.values()), json_file, ensure_ascii=False, indent=4)


def main(pages, skill=None):
    driver = setup_selenium()

    try:
        if skill:
            base_url = f"https://robota.ua/candidates/{skill}/ukraine"
        else:
            base_url = "https://robota.ua/candidates/all/ukraine"

        for page in tqdm(range(1, pages + 1), desc="Processing pages"):
            url = f"{base_url}?page={page}"
            print(f"\nProcessing page {page}...")

            sleep_time = random.randint(5, 20)
            print(f"Waiting {sleep_time} seconds...")
            time.sleep(sleep_time)

            resumes = fetch_resumes(url, driver)
            print(f"Found {len(resumes)} resumes on page {page}.")

            if not resumes:
                print(f"No resumes found on page {page}. Stopping.")
                break

            save_to_json(resumes, 'resumes_robota_ua.json')

        print("Data saved to resumes_robota_ua.json")
    finally:
        driver.quit()


if __name__ == "__main__":
    # python robota_ua/get_resume.py --pages 2 --skill python
    parser = argparse.ArgumentParser(description="Parse resume listings.")
    parser.add_argument('--pages', type=int, default=2,
                        help='Number of pages to process (default: 2)')
    parser.add_argument('--skill', type=str, default=None,
                        help='Search keyword, for example "python"')
    args = parser.parse_args()
    main(args.pages, args.skill)
