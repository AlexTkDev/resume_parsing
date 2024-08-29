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
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from tqdm import tqdm


def setup_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Работать в фоновом режиме
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def fetch_resumes(url, driver):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'section.cv-card'))
    )

    resumes = driver.find_elements(By.CSS_SELECTOR, 'section.cv-card')
    resume_list = []

    for resume in resumes:
        try:
            title = resume.find_element(By.CSS_SELECTOR, 'p[data-id="cv-speciality"]').text.strip()
        except NoSuchElementException:
            title = 'No title'

        try:
            link = resume.find_element(
                By.CSS_SELECTOR, 'a.santa-no-underline').get_attribute('href')
        except NoSuchElementException:
            link = 'No link'

        try:
            name = resume.find_element(
                By.CSS_SELECTOR, 'p.santa-typo-regular.santa-truncate').text.strip()
        except NoSuchElementException:
            name = 'No name'

        try:
            details = resume.find_element(
                By.CSS_SELECTOR, 'div.santa-flex.santa-items-center.santa-space-x-10'
                                 '.santa-pr-20.santa-whitespace-nowrap').text.strip()
        except NoSuchElementException:
            details = 'No details'

        try:
            posted_time = resume.find_element(
                By.CSS_SELECTOR, 'p.santa-typo-additional.santa-text-black-500').text.strip()
        except NoSuchElementException:
            posted_time = 'No time'

        resume_data = {
            "title": title,
            "link": link,
            "name": name,
            "details": details,
            "posted_time": posted_time
        }

        resume_list.append(resume_data)

    return resume_list


def save_to_json(data, filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
        existing_data.extend(data)
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
    else:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)


def main(pages, skill=None):
    driver = setup_selenium()

    if skill:
        base_url = f"https://robota.ua/candidates/{skill}/ukraine"
    else:
        base_url = "https://robota.ua/candidates/all/ukraine"

    for page in tqdm(range(1, pages + 1), desc="Обработка страниц"):
        url = f"{base_url}?page={page}"
        print(f"\nОбрабатываю страницу {page}...")

        sleep_time = random.randint(5, 20)
        print(f"Ожидание {sleep_time} секунд...")
        time.sleep(sleep_time)

        resumes = fetch_resumes(url, driver)
        print(f"Найдено {len(resumes)} резюме на странице {page}.")

        if not resumes:
            print(f"Нет резюме на странице {page}. Завершаю...")
            break

        save_to_json(resumes, 'resumes_robota_ua.json')

    driver.quit()
    print("Данные успешно сохранены в resumes_robota_ua.json")


if __name__ == "__main__":
    # python robota_ua/get_resume.py --pages 2 --skill python
    parser = argparse.ArgumentParser(description="Скрипт для парсинга резюме.")
    parser.add_argument('--pages', type=int, default=2,
                        help='Количество страниц для обхода (по умолчанию 2)')
    parser.add_argument('--skill', type=str, default=None,
                        help='Ключевое слово для поиска (например, "python")')
    args = parser.parse_args()
    main(args.pages, args.skill)
