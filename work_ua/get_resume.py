import argparse
import logging
import random
import time
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from tqdm import tqdm
from utils.utils import fetch_html, save_json, load_yaml, setup_logging

CONFIG_PATH = 'utils/config.yaml'
OUTPUT_FILE = 'resumes_work_ua.json'


def fetch_resumes(url: str, selectors: Dict[str, str]) -> List[Dict[str, Any]]:
    """Парсит резюме с одной страницы work.ua."""
    html = fetch_html(url)
    if not html:
        logging.warning(f'Не удалось загрузить страницу: {url}')
        return []
    soup = BeautifulSoup(html, 'html.parser')
    resumes = soup.find_all('div', class_=selectors['card'])
    resume_list = []
    for resume in resumes:
        title = resume.find('h2').text.strip() if resume.find('h2') else 'No title'
        link = resume.find('a')['href'] if resume.find('a') else 'No link'
        name = resume.find('span', class_=selectors['name']).text.strip() if resume.find('span', class_=selectors['name']) else 'No name'
        details = resume.find('p', class_=selectors['details']).text.strip() if resume.find('p', class_=selectors['details']) else 'No details'
        posted_time = resume.find('time').text.strip() if resume.find('time') else 'No time'
        resume_data = {
            "title": title,
            "link": f"https://www.work.ua{link}",
            "name": name,
            "details": details,
            "posted_time": posted_time
        }
        resume_list.append(resume_data)
    return resume_list


def main(pages: int, skill: str = "") -> None:
    setup_logging()
    config = load_yaml(CONFIG_PATH)
    selectors = {
        'card': 'card card-hover card-search resume-link card-visited wordwrap',
        'name': 'strong-600',
        'details': 'mb-0 overflow wordwrap',
    }
    if skill:
        base_url = f"https://www.work.ua/resumes-{skill}/"
    else:
        base_url = "https://www.work.ua/resumes/?ss=1"
    all_resumes = []
    for page in tqdm(range(1, pages + 1), desc="Обработка страниц"):
        url = f"{base_url}?page={page}"
        logging.info(f"Обрабатываю страницу {page}: {url}")
        sleep_time = random.randint(5, 20)
        logging.info(f"Ожидание {sleep_time} секунд...")
        time.sleep(sleep_time)
        resumes = fetch_resumes(url, selectors)
        if not resumes:
            logging.info(f"Нет резюме на странице {page}. Завершаю...")
            break
        all_resumes.extend(resumes)
        save_json(all_resumes, OUTPUT_FILE)
    logging.info(f"Данные успешно сохранены в {OUTPUT_FILE}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрипт для парсинга резюме с work.ua.")
    parser.add_argument('--pages', type=int, default=5, help='Количество страниц для обхода (по умолчанию 5)')
    parser.add_argument('--skill', type=str, default=None, help='Ключевое слово для поиска (например, "python")')
    args = parser.parse_args()
    main(args.pages, args.skill)
