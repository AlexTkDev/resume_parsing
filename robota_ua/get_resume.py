import argparse
import logging
import random
import time
from typing import List, Dict, Any
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import setup_selenium, save_json, load_yaml, setup_logging

CONFIG_PATH = 'utils/config.yaml'
OUTPUT_FILE = 'resumes_robota_ua.json'


def fetch_resumes(url: str, driver, selectors: Dict[str, str]) -> List[Dict[str, Any]]:
    """Парсит резюме с одной страницы robota.ua с помощью Selenium."""
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selectors['card']))
        )
    except Exception as e:
        logging.warning(f'Не удалось дождаться загрузки страницы: {url} ({e})')
        return []
    resumes = driver.find_elements(By.CSS_SELECTOR, selectors['card'])
    resume_list = []
    for resume in resumes:
        def safe_find(selector, by=By.CSS_SELECTOR, attr=None):
            try:
                el = resume.find_element(by, selector)
                return el.get_attribute(attr) if attr else el.text.strip()
            except NoSuchElementException:
                return f'No {attr or selector}'
        title = safe_find(selectors['title'])
        link = safe_find(selectors['link'], attr='href')
        name = safe_find(selectors['name'])
        details = safe_find(selectors['details'])
        posted_time = safe_find(selectors['posted_time'])
        resume_data = {
            "title": title,
            "link": link,
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
        'card': 'section.cv-card',
        'title': 'p[data-id="cv-speciality"]',
        'link': 'a.santa-no-underline',
        'name': 'p.santa-typo-regular.santa-truncate',
        'details': 'div.santa-flex.santa-items-center.santa-space-x-10.santa-pr-20.santa-whitespace-nowrap',
        'posted_time': 'p.santa-typo-additional.santa-text-black-500',
    }
    driver = setup_selenium()
    try:
        if skill:
            base_url = f"https://robota.ua/candidates/{skill}/ukraine"
        else:
            base_url = "https://robota.ua/candidates/all/ukraine"
        all_resumes = []
        for page in tqdm(range(1, pages + 1), desc="Обработка страниц"):
            url = f"{base_url}?page={page}"
            logging.info(f"Обрабатываю страницу {page}: {url}")
            sleep_time = random.randint(5, 20)
            logging.info(f"Ожидание {sleep_time} секунд...")
            time.sleep(sleep_time)
            resumes = fetch_resumes(url, driver, selectors)
            logging.info(f"Найдено {len(resumes)} резюме на странице {page}.")
            if not resumes:
                logging.info(f"Нет резюме на странице {page}. Завершаю...")
                break
            all_resumes.extend(resumes)
            save_json(all_resumes, OUTPUT_FILE)
        logging.info(f"Данные успешно сохранены в {OUTPUT_FILE}")
    finally:
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрипт для парсинга резюме с robota.ua.")
    parser.add_argument('--pages', type=int, default=2, help='Количество страниц для обхода (по умолчанию 2)')
    parser.add_argument('--skill', type=str, default=None, help='Ключевое слово для поиска (например, "python")')
    args = parser.parse_args()
    main(args.pages, args.skill)
