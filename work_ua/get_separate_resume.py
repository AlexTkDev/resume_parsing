import requests
from bs4 import BeautifulSoup
import json
import argparse


def clean_text(text):
    """Убирает лишние пробелы и символы переноса строк."""
    return ' '.join(text.split())


def get_separate_resume(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    resume = soup.find('div', class_='card wordwrap mt-0')

    if not resume:
        return []

    title = resume.find('h2', class_="mt-lg sm:mt-xl")
    title_text = title.text.strip() if title else 'No title'

    name = resume.find('h1')
    name_text = name.text.strip() if name else 'No name'

    details = resume.find('div', class_='wordwrap')
    details_text = clean_text(details.get_text()) if details else 'No details'

    final_resume_data = {
        "title": title_text,
        "name": name_text,
        "details": details_text,
    }

    return [final_resume_data]


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def main(user_id):
    if user_id is None:
        print("Please provide a valid user ID.")
        return

    base_url = f"https://www.work.ua/resumes/{user_id}/"
    print(f'Processing page: {base_url}')

    resume = get_separate_resume(base_url)
    save_to_json(resume, f'resume_{user_id}.json')


if __name__ == "__main__":
    # python work_ua/get_separate_resume.py --userID 10856921
    parser = argparse.ArgumentParser(description="Скрипт для парсинга резюме.")
    parser.add_argument('--userID', type=int, required=True, help='ID пользователя')
    args = parser.parse_args()
    main(args.userID)
