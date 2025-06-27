import os
import re
import argparse
import logging
from typing import Dict
from utils.utils import load_yaml, setup_logging, clean_text

CONFIG_PATH = 'utils/config.yaml'


def extract_experience_years(resume_text: str) -> int:
    """Извлекает общее количество лет опыта из текста резюме."""
    matches = re.findall(r'(\d+)\s+years?', resume_text)
    if not matches:
        # Украинская версия
        matches = re.findall(r'(\d+)\s+років', resume_text)
    years = sum(int(match) for match in matches)
    return years


def score_resume(resume_text: str, config: Dict) -> int:
    """Оценивает резюме по критериям из config."""
    score = 0
    resume_text = clean_text(resume_text)
    # Определяем источник по наличию секций
    if any(section in resume_text for section in config['sections']['robota_ua']):
        sections = config['sections']['robota_ua']
        for section in sections:
            if section in resume_text:
                score += config['weights']['section_found']
            else:
                score += config['weights']['section_missing']
    else:
        sections = config['sections']['work_ua']
        for section in sections:
            if section in resume_text:
                score += config['weights']['section_found'] // 2
            else:
                score += config['weights']['section_missing']
    # Ключевые слова
    for keyword in config['keywords']:
        if re.search(rf'\b{re.escape(keyword)}\b', resume_text, re.IGNORECASE):
            score += config['weights']['keyword']
    # Опыт работы
    experience_years = extract_experience_years(resume_text)
    if experience_years >= 5:
        score += config['weights']['experience']['more_than_5']
    elif 3 <= experience_years < 5:
        score += config['weights']['experience']['between_3_and_5']
    elif experience_years < 3 and experience_years > 0:
        score += config['weights']['experience']['less_than_3']
    # Образование
    if re.search(r'(Bachelor|Master|MCA|BCA|Computer Science|Engineering)', resume_text, re.IGNORECASE):
        score += config['weights']['education']
    # Сертификаты, курсы
    score += len(re.findall(r'(certificate|course)', resume_text, re.IGNORECASE)) * config['weights']['certificate']
    return score


def load_resumes(resume_folder: str) -> Dict[str, str]:
    """Загружает все резюме из папки."""
    resumes = {}
    for filename in os.listdir(resume_folder):
        if filename.endswith('.txt'):
            try:
                with open(os.path.join(resume_folder, filename), 'r', encoding='utf-8') as file:
                    resumes[filename] = file.read()
            except Exception as e:
                logging.error(f"Ошибка при чтении {filename}: {e}")
    return resumes


def sort_candidates_by_relevance(resumes: Dict[str, str], config: Dict) -> list:
    """Сортирует резюме по релевантности."""
    scored_resumes = {}
    for filename, text in resumes.items():
        score = score_resume(text, config)
        scored_resumes[filename] = score
    sorted_resumes = sorted(scored_resumes.items(), key=lambda item: item[1], reverse=True)
    return sorted_resumes


def main(resume_folder: str) -> None:
    setup_logging()
    config = load_yaml(CONFIG_PATH)
    resumes = load_resumes(resume_folder)
    sorted_candidates = sort_candidates_by_relevance(resumes, config)
    with open('sorted_candidates.txt', 'w', encoding='utf-8') as txt_file:
        for filename, score in sorted_candidates:
            resume_path = os.path.abspath(os.path.join(resume_folder, filename))
            txt_file.write(f'{filename}: {score} баллов\nСсылка на резюме: {resume_path}\n\n')
    logging.info(f'Сортировка завершена. Результаты сохранены в sorted_candidates.txt')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Оценка и сортировка резюме")
    parser.add_argument("--directory", type=str, required=True, help="Папка с резюме")
    args = parser.parse_args()
    main(args.directory)

