import requests
import json
import os
import time
import random
import argparse

from tqdm import tqdm

from html_stream_parser import parse_resume_listings

REQUEST_TIMEOUT = 20
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


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


def fetch_resumes(url):
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Request failed for {url}: {exc}")
        return []

    return parse_resume_listings(response.text)


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
    if skill:
        base_url = f"https://www.work.ua/resumes-{skill}/"
    else:
        base_url = "https://www.work.ua/resumes/?ss=1"

    for page in tqdm(range(1, pages + 1), desc="Processing pages"):
        separator = '&' if '?' in base_url else '?'
        url = f"{base_url}{separator}page={page}"
        print(f"\nProcessing page {page}...")

        sleep_time = random.randint(5, 20)
        print(f"Waiting {sleep_time} seconds...")
        time.sleep(sleep_time)

        resumes = fetch_resumes(url)

        if not resumes:
            print(f"No resumes found on page {page}. Stopping.")
            break

        save_to_json(resumes, 'resumes_work_ua.json')

    print("Data saved to resumes_work_ua.json")


if __name__ == "__main__":
    #  python work_ua/get_resume.py --pages 2 --skill python
    parser = argparse.ArgumentParser(description="Parse resume listings.")
    parser.add_argument('--pages', type=int, default=5,
                        help='Number of pages to process (default: 5)')
    parser.add_argument('--skill', type=str, default=None,
                        help='Search keyword, for example "python"')
    args = parser.parse_args()
    main(args.pages, args.skill)
