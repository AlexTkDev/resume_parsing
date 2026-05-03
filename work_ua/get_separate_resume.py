import requests
import json
import argparse
import os
from urllib.parse import urlparse

from html_stream_parser import parse_resume_page

REQUEST_TIMEOUT = 20
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


def get_user_links(file):
    """Extract all link values from a JSON file."""
    links = []
    if not os.path.exists(file) or os.path.getsize(file) == 0:
        print(f"No data found in {file}.")
        return links

    try:
        with open(file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        print(f"Invalid JSON in {file}.")
        return links

    if not isinstance(data, list):
        print(f"{file} must contain a JSON list.")
        return links

    for item in data:
        if isinstance(item, dict) and item.get('link') and item['link'] != 'No link':
            links.append(item['link'])
    return links


def get_separate_resume(url):
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Request failed for {url}: {exc}")
        return "No resume found."

    return parse_resume_page(response.text)


def save_to_txt(data, filename):
    """Save extracted resume data as a text file."""
    with open(filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(data)


def main(file):
    links = get_user_links(file)
    if not links:
        print("No links found in the file.")
        return

    output_dir = 'ready-made_resumes'
    os.makedirs(output_dir, exist_ok=True)

    for link in links:
        print(f'Processing page: {link}')
        resume = get_separate_resume(link)
        user_id = urlparse(link).path.rstrip('/').split('/')[-1] or "unknown"
        save_to_txt(resume, os.path.join(output_dir, f'resume_{user_id}.txt'))


if __name__ == "__main__":
    #   python work_ua/get_separate_resume.py --file resumes_work_ua.json
    parser = argparse.ArgumentParser(description="Export separate resume files.")
    parser.add_argument('--file', type=str, required=True,
                        help='JSON file with resume links')
    args = parser.parse_args()
    main(args.file)
