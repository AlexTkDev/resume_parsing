import argparse
import logging
import os
from typing import List
from bs4 import BeautifulSoup
from utils.utils import clean_text, fetch_html, setup_logging

OUTPUT_DIR = 'ready-made_resumes'


def get_user_links(file: str) -> List[str]:
    """Извлекает все значения ключа 'link' из JSON-файла."""
    import json
    links = []
    with open(file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for item in data:
            if 'link' in item:
                links.append(item['link'])
    return links


def get_separate_resume(url: str) -> str:
    """Парсит отдельное резюме по ссылке."""
    html = fetch_html(url)
    if not html:
        logging.warning(f'Не удалось загрузить страницу: {url}')
        return "No resume found."
    soup = BeautifulSoup(html, 'html.parser')
    resume = soup.select_one('div.card.wordwrap.mt-0')
    if not resume:
        return "No resume found."
    title = resume.select_one('h2.mt-lg') or resume.select_one('h2.sm\\:mt-xl')
    title_text = title.text.strip() if title else 'No title'
    name = resume.select_one('h1')
    name_text = name.text.strip() if name else 'No name'
    details = resume.select_one('div.wordwrap')
    details_text = clean_text(details.get_text()) if details else 'No details'
    final_resume_data = f"Title: {title_text}\nName: {name_text}\nDetails: {details_text}\n"
    return final_resume_data


def save_to_txt(data: str, filename: str) -> None:
    """Сохраняет данные в текстовом формате .txt."""
    with open(filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(data)


def main(file: str) -> None:
    setup_logging()
    links = get_user_links(file)
    if not links:
        logging.warning("No links found in the file.")
        return
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for link in links:
        logging.info(f'Processing page: {link}')
        resume = get_separate_resume(link)
        user_id = link.split('/')[-2]  # userID из URL
        save_to_txt(resume, os.path.join(OUTPUT_DIR, f'resume_{user_id}.txt'))
    logging.info(f'Готово. Все резюме сохранены в {OUTPUT_DIR}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрипт для парсинга отдельного резюме с work.ua.")
    parser.add_argument('--file', type=str, required=True, help='JSON файл со ссылками на резюме')
    args = parser.parse_args()
    main(args.file)
