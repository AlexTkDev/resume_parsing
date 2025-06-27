import argparse
import logging
import os
from typing import List, Dict, Tuple
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import setup_selenium, clean_text, setup_logging

OUTPUT_DIR = 'ready-made_resumes'


def get_user_data(file: str) -> List[Dict[str, str]]:
    """Извлекает ссылки и имена кандидатов из JSON-файла."""
    import json
    user_data = []
    with open(file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for item in data:
            if 'link' in item and 'name' in item:
                user_data.append({'link': item['link'], 'name': item['name']})
    return user_data


def get_separate_resume(driver, url: str) -> Tuple[str, str]:
    """Извлекает информацию из резюме по URL."""
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'alliance-shared-ui-prof-resume-experience'))
        )
        def safe_find(selector, by=By.CSS_SELECTOR):
            try:
                el = driver.find_element(by, selector)
                return el.text if el.text else None
            except NoSuchElementException:
                return None
        experience = clean_text(safe_find('alliance-shared-ui-prof-resume-experience') or "No experience information provided.")
        skills = clean_text(safe_find('alliance-shared-ui-prof-resume-skill-summary') or "No skills information provided.")
        education = clean_text(safe_find('alliance-shared-ui-prof-resume-education') or "No education information provided.")
        languages = clean_text(safe_find('alliance-shared-ui-prof-resume-languages') or "No languages information provided.")
        try:
            additional_info_section = driver.find_element(By.XPATH, "//section[h3[contains(text(), 'Додаткова інформація')]]")
            additional_info = clean_text(additional_info_section.find_element(By.CSS_SELECTOR, 'div.santa-list').text)
        except NoSuchElementException:
            additional_info = "No additional information provided."
        try:
            courses_section = driver.find_element(By.CSS_SELECTOR, 'alliance-shared-ui-prof-resume-courses')
            courses = clean_text(courses_section.find_element(By.CSS_SELECTOR, 'div.santa-mb-20').text)
        except NoSuchElementException:
            courses = "No courses, trainings, or certificates provided."
        resume_data = (
            f"Experience:\n{experience}\n\n"
            f"Skills:\n{skills}\n\n"
            f"Education:\n{education}\n\n"
            f"Languages:\n{languages}\n\n"
            f"Additional Information:\n{additional_info}"
        )
        return resume_data, courses
    except Exception as e:
        logging.error(f"Error extracting data from {url}: {e}")
        return "", "No courses, trainings, or certificates provided."


def save_to_txt(resume_data: str, courses_data: str, filename: str) -> None:
    """Сохраняет данные в текстовом формате .txt."""
    with open(filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(f"{resume_data}\n\nCourses, trainings, certificates:\n{courses_data}")


def main(file: str) -> None:
    setup_logging()
    driver = setup_selenium()
    user_data = get_user_data(file)
    if not user_data:
        logging.warning("No user data found in the file.")
        driver.quit()
        return
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        for data in user_data:
            link = data['link']
            logging.info(f'Processing page: {link}')
            resume, courses = get_separate_resume(driver, link)
            user_id = link.split('/')[-1]
            filename = os.path.join(OUTPUT_DIR, f'resume_{user_id}.txt')
            save_to_txt(resume, courses, filename)
        logging.info(f'Готово. Все резюме сохранены в {OUTPUT_DIR}')
    finally:
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрипт для парсинга отдельного резюме с robota.ua.")
    parser.add_argument('--file', type=str, required=True, help='JSON файл с данными кандидатов')
    args = parser.parse_args()
    main(args.file)
