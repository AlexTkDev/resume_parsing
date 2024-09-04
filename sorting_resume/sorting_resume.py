import os
import re
import argparse


def score_resume(resume_text):
    score = 0

    # Полнота резюме для разных структур
    # robota.ua
    if 'Experience' in resume_text or 'Skills' in resume_text or 'Education' in resume_text:
        sections = ['Experience', 'Skills', 'Education', 'Languages', 'Additional Information',
                    'Courses, trainings, certificates']
        for section in sections:
            if section in resume_text:
                score += 10
            else:
                score -= 2
    # work.ua
    else:
        basic_sections = ['Title', 'Name', 'Details']
        for section in basic_sections:
            if section in resume_text:
                score += 5
            else:
                score -= 2

    # Ключевые слова
    keywords = ['Python', 'Django', 'REST API', 'SQL', 'JavaScript', 'Docker', 'AWS']
    for keyword in keywords:
        if re.search(rf'\b{keyword}\b', resume_text, re.IGNORECASE):
            score += 5

    # Опыт работы
    experience_years = extract_experience_years(resume_text)
    if experience_years >= 5:
        score += 15
    elif 3 <= experience_years < 5:
        score += 10
    elif experience_years < 3:
        score += 5

    # Образование
    if re.search(r'(Bachelor|Master|MCA|BCA|Computer Science|Engineering)', resume_text,
                 re.IGNORECASE):
        score += 5

    # Дополнительные критерии: сертификаты, курсы
    if 'certificates' in resume_text.lower() or 'courses' in resume_text.lower():
        score += len(re.findall(r'(certificate|course)', resume_text, re.IGNORECASE)) * 3

    return score


def extract_experience_years(resume_text):
    """Функция для извлечения общего количества лет опыта из резюме."""
    matches = re.findall(r'(\d+)\s+years?', resume_text)
    if not matches:
        # Украинская версия
        matches = re.findall(r'(\d+)\s+років', resume_text)
    years = sum(int(match) for match in matches)
    return years


def load_resumes(resume_folder):
    resumes = {}
    for filename in os.listdir(resume_folder):
        if filename.endswith('.txt'):
            with open(os.path.join(resume_folder, filename), 'r', encoding='utf-8') as file:
                resumes[filename] = file.read()
    return resumes


def sort_candidates_by_relevance(resumes):
    scored_resumes = {}
    for filename, text in resumes.items():
        score = score_resume(text)
        scored_resumes[filename] = score

    # Сортировка по убыванию баллов
    sorted_resumes = sorted(scored_resumes.items(), key=lambda item: item[1], reverse=True)
    return sorted_resumes


def main(resume_folder):
    resumes = load_resumes(resume_folder)
    sorted_candidates = sort_candidates_by_relevance(resumes)

    with open('sorted_candidates.txt', 'w', encoding='utf-8') as txt_file:
        for filename, score in sorted_candidates:
            # Полный путь к резюме
            resume_path = os.path.abspath(os.path.join(resume_folder, filename))
            txt_file.write(f'{filename}: {score} баллов\nСсылка на резюме: {resume_path}\n\n')


if __name__ == "__main__":
    # python sorting_resume/sorting_resume.py --directory ready-made_resumes
    parser = argparse.ArgumentParser(description="Оценка резюме")
    parser.add_argument("--directory", type=str, required=True,
                        help="Папка с резюме")
    args = parser.parse_args()
    main(args.directory)
