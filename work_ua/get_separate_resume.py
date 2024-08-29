import requests
from bs4 import BeautifulSoup
import json
import argparse
import os


def get_user_links(file):
    """Извлекает все значения ключа 'link' из JSON-файла."""
    links = []
    with open(file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for item in data:
            if 'link' in item:
                links.append(item['link'])
    return links


def clean_text(text):
    """Убирает лишние пробелы и символы переноса строк."""
    return ' '.join(text.split())


def get_separate_resume(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    resume = soup.find('div', class_='card wordwrap mt-0')

    if not resume:
        return "No resume found."

    title = resume.find('h2', class_="mt-lg sm:mt-xl")
    title_text = title.text.strip() if title else 'No title'

    name = resume.find('h1')
    name_text = name.text.strip() if name else 'No name'

    details = resume.find('div', class_='wordwrap')
    details_text = clean_text(details.get_text()) if details else 'No details'

    final_resume_data = f"Title: {title_text}\nName: {name_text}\nDetails: {details_text}\n"

    return final_resume_data


def save_to_txt(data, filename):
    """Сохраняем данные в текстовом формате .txt."""
    with open(filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(data)


def main(file):
    links = get_user_links(file)
    if not links:
        print("No links found in the file.")
        return

    # Создание папки для сохранения резюме, если её нет
    output_dir = 'ready-made_resumes'
    os.makedirs(output_dir, exist_ok=True)

    for link in links:
        print(f'Processing page: {link}')
        resume = get_separate_resume(link)
        user_id = link.split('/')[-2]  # извлечение userID из URL для имени
        save_to_txt(resume, os.path.join(output_dir, f'resume_{user_id}.txt'))


if __name__ == "__main__":
    #   python work_ua/get_separate_resume.py --file resumes_work_ua.json
    parser = argparse.ArgumentParser(description="Скрипт для парсинга резюме.")
    parser.add_argument('--file', type=str, required=True,
                        help='JSON файл со ссылками на резюме')
    args = parser.parse_args()
    main(args.file)
