import argparse
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


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
    """Извлекает ссылки и имена кандидатов из JSON-файла."""
    user_data = []
    with open(file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for item in data:
            if 'link' in item and 'name' in item:
                user_data.append({
                    'link': item['link'],
                    'name': item['name']
                })
    return user_data


def clean_text(text):
    """Убирает лишние пробелы и символы переноса строк."""
    return ' '.join(text.split())


def get_separate_resume(driver, url):
    """Извлекает информацию из резюме по URL."""
    driver.get(url)

    try:
        # Ожидание загрузки контента
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'alliance-shared-ui-prof-resume-experience'))
        )

        # Извлечение информации
        try:
            experience_element = driver.find_element(
                By.CSS_SELECTOR, 'alliance-shared-ui-prof-resume-experience')
            experience = experience_element.text \
                if experience_element.text else "No experience information provided."
        except NoSuchElementException:
            experience = "No experience information provided."

        try:
            skills_element = driver.find_element(
                By.CSS_SELECTOR, 'alliance-shared-ui-prof-resume-skill-summary')
            skills = skills_element.text \
                if skills_element.text else "No skills information provided."
        except NoSuchElementException:
            skills = "No skills information provided."

        try:
            education_element = driver.find_element(
                By.CSS_SELECTOR, 'alliance-shared-ui-prof-resume-education')
            education = education_element.text \
                if education_element.text else "No education information provided."
        except NoSuchElementException:
            education = "No education information provided."

        try:
            languages_element = driver.find_element(
                By.CSS_SELECTOR, 'alliance-shared-ui-prof-resume-languages')
            languages = languages_element.text \
                if languages_element.text else "No languages information provided."
        except NoSuchElementException:
            languages = "No languages information provided."

        try:
            additional_info_section = driver.find_element(
                By.XPATH, "//section[h3[contains(text(), 'Додаткова інформація')]]")
            additional_info = additional_info_section.find_element(
                By.CSS_SELECTOR, 'div.santa-list').text
        except NoSuchElementException:
            additional_info = "No additional information provided."

        try:
            courses_section = driver.find_element(
                By.CSS_SELECTOR, 'alliance-shared-ui-prof-resume-courses')
            courses = courses_section.find_element(By.CSS_SELECTOR, 'div.santa-mb-20').text
            courses_data = clean_text(courses)
        except NoSuchElementException:
            courses_data = "No courses, trainings, or certificates provided."

        # Компоновка данных
        resume_data = (f"Experience:\n{clean_text(experience)}\n\n"
                       f"Skills:\n{clean_text(skills)}\n\n"
                       f"Education:\n{clean_text(education)}\n\n"
                       f"Languages:\n{clean_text(languages)}\n\n"
                       f"Additional Information:\n{clean_text(additional_info)}")

        return resume_data, courses_data
    except NoSuchElementException as e:
        print(f"Error extracting data from {url}: {e}")
        return "", "No courses, trainings, or certificates provided."


def save_to_txt(resume_data, courses_data, filename):
    """Сохраняем данные в текстовом формате .txt."""
    with open(filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(f"{resume_data}\n\nCourses, trainings, certificates:\n{courses_data}")


def main(file):
    driver = setup_selenium()
    user_data = get_user_data(file)

    if not user_data:
        print("No user data found in the file.")
        driver.quit()
        return

    # Создание папки для сохранения резюме, если её нет
    output_dir = 'ready-made_resumes'
    os.makedirs(output_dir, exist_ok=True)

    for data in user_data:
        link = data['link']
        print(f'Processing page: {link}')
        resume, courses = get_separate_resume(driver, link)

        # Извлечение ID из URL
        user_id = link.split('/')[-1]

        # Создание имени файла
        filename = os.path.join(output_dir, f'resume_{user_id}.txt')
        save_to_txt(resume, courses, filename)

    driver.quit()


if __name__ == "__main__":
    # python robota_ua/get_separate_resume.py --file resumes_robota_ua.json
    parser = argparse.ArgumentParser(description="Скрипт для парсинга резюме.")
    parser.add_argument('--file', type=str, required=True,
                        help='JSON файл с данными кандидатов')
    args = parser.parse_args()
    main(args.file)
