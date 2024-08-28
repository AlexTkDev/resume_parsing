import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random
import argparse
from tqdm import tqdm


def fetch_resumes(url):
    # Выполняем GET запрос
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    resumes = soup.find_all('div',
                            class_='card card-hover card-search resume-link card-visited wordwrap')
    resume_list = []

    for resume in resumes:
        title = resume.find('h2').text.strip() if resume.find('h2') else 'No title'
        link = resume.find('a')['href'] if resume.find('a') else 'No link'
        name = resume.find(
            'span', class_='strong-600').text.strip() if resume.find(
            'span', class_='strong-600') else 'No name'
        details = resume.find(
            'p', class_='mb-0 overflow wordwrap').text.strip() if resume.find(
            'p', class_='mb-0 overflow wordwrap') else 'No details'
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


def save_to_json(data, filename):
    # Если файл уже существует, добавляем данные к существующим
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
        existing_data.extend(data)
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
    else:
        # Сохраняем данные в новый JSON файл
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)


def main(pages, skill=None):
    if skill:
        base_url = f"https://www.work.ua/resumes-{skill}/"
    else:
        base_url = "https://www.work.ua/resumes/?ss=1"

    for page in tqdm(range(1, pages + 1), desc="Обработка страниц"):
        url = f"{base_url}?page={page}"
        print(f"\nОбрабатываю страницу {page}...")

        # Случайный таймслип от 5 до 20 секунд
        sleep_time = random.randint(5, 20)
        print(f"Ожидание {sleep_time} секунд...")
        time.sleep(sleep_time)

        resumes = fetch_resumes(url)

        if not resumes:
            print(f"Нет резюме на странице {page}. Завершаю...")
            break

        save_to_json(resumes, 'resumes_work_ua.json')

    print("Данные успешно сохранены в resumes_work_ua.json")


if __name__ == "__main__":
    #  python work_ua/get_resume.py --pages 2 --skill python
    parser = argparse.ArgumentParser(description="Скрипт для парсинга резюме.")
    parser.add_argument('--pages', type=int, default=5,
                        help='Количество страниц для обхода (по умолчанию 5)')
    parser.add_argument('--skill', type=str, default=None,
                        help='Ключевое слово для поиска (например, "python")')
    args = parser.parse_args()
    main(args.pages, args.skill)
