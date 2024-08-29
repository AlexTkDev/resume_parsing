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
        experience = driver.find_element(By.CSS_SELECTOR,
                                         'alliance-shared-ui-prof-resume-experience').text
        skills = driver.find_element(By.CSS_SELECTOR,
                                     'alliance-shared-ui-prof-resume-skill-summary').text
        education = driver.find_element(By.CSS_SELECTOR,
                                        'alliance-shared-ui-prof-resume-education').text
        languages = driver.find_element(By.CSS_SELECTOR,
                                        'alliance-shared-ui-prof-resume-languages').text

        # Компоновка данных
        resume_data = (f"Experience:\n{clean_text(experience)}\n\nSkills:\n{clean_text(skills)}"
                       f"\n\nEducation:\n{clean_text(education)}\n\nLanguages:"
                       f"\n{clean_text(languages)}")

        return resume_data
    except NoSuchElementException as e:
        print(f"Error extracting data from {url}: {e}")
        return ""


def save_to_txt(data, filename):
    """Сохраняем данные в текстовом формате .txt."""
    with open(filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(data)


def main(file):
    driver = setup_selenium()

    user_data = get_user_data(file)
    if not user_data:
        print("No user data found in the file.")
        return

    # Создание папки для сохранения резюме, если её нет
    output_dir = 'ready-made_resumes'
    os.makedirs(output_dir, exist_ok=True)

    for data in user_data:
        link = data['link']
        name = data['name']
        print(f'Processing page: {link}')
        resume = get_separate_resume(driver, link)

        # Извлечение ID из URL
        user_id = link.split('/')[-1]

        # Создание имени файла
        filename = os.path.join(output_dir, f'resume_{user_id}.txt')
        save_to_txt(resume, filename)

    driver.quit()


if __name__ == "__main__":
    # python robota_ua/get_separate_resume.py --file resumes_robota_ua.json
    parser = argparse.ArgumentParser(description="Скрипт для парсинга резюме.")
    parser.add_argument('--file', type=str, required=True,
                        help='JSON файл с данными кандидатов')
    args = parser.parse_args()
    main(args.file)
