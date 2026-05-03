import os
import re
import argparse


def score_resume(resume_text):
    score = 0

    if 'Experience' in resume_text or 'Skills' in resume_text or 'Education' in resume_text:
        sections = ['Experience', 'Skills', 'Education', 'Languages', 'Additional Information',
                    'Courses, trainings, certificates']
        for section in sections:
            if section in resume_text:
                score += 10
            else:
                score -= 2
    else:
        basic_sections = ['Title', 'Name', 'Details']
        for section in basic_sections:
            if section in resume_text:
                score += 5
            else:
                score -= 2

    keywords = ['Python', 'Django', 'REST API', 'SQL', 'JavaScript', 'Docker', 'AWS']
    for keyword in keywords:
        if re.search(rf'\b{keyword}\b', resume_text, re.IGNORECASE):
            score += 5

    experience_years = extract_experience_years(resume_text)
    if experience_years >= 5:
        score += 15
    elif 3 <= experience_years < 5:
        score += 10
    elif experience_years < 3:
        score += 5

    if re.search(r'(Bachelor|Master|MCA|BCA|Computer Science|Engineering)', resume_text,
                 re.IGNORECASE):
        score += 5

    if 'certificates' in resume_text.lower() or 'courses' in resume_text.lower():
        score += len(re.findall(r'(certificate|course)', resume_text, re.IGNORECASE)) * 3

    return score


def extract_experience_years(resume_text):
    """Extract total years of experience from common English and Ukrainian forms."""
    matches = re.findall(
        r'(\d+)\+?\s*(?:years?|yrs?|років|роки|рік)',
        resume_text,
        re.IGNORECASE,
    )
    years = sum(int(match) for match in matches)
    return years


def load_resumes(resume_folder):
    if not os.path.isdir(resume_folder):
        raise FileNotFoundError(f"Resume directory does not exist: {resume_folder}")

    resumes = {}
    for filename in sorted(os.listdir(resume_folder)):
        if filename.endswith('.txt'):
            with open(os.path.join(resume_folder, filename), 'r', encoding='utf-8') as file:
                resumes[filename] = file.read()
    return resumes


def sort_candidates_by_relevance(resumes):
    scored_resumes = {}
    for filename, text in resumes.items():
        score = score_resume(text)
        scored_resumes[filename] = score

    sorted_resumes = sorted(scored_resumes.items(), key=lambda item: (-item[1], item[0].lower()))
    return sorted_resumes


def main(resume_folder):
    resumes = load_resumes(resume_folder)
    sorted_candidates = sort_candidates_by_relevance(resumes)

    with open('sorted_candidates.txt', 'w', encoding='utf-8') as txt_file:
        for filename, score in sorted_candidates:
            resume_path = os.path.abspath(os.path.join(resume_folder, filename))
            txt_file.write(f'{filename}: {score} points\nResume path: {resume_path}\n\n')


if __name__ == "__main__":
    # python sorting_resume/sorting_resume.py --directory ready-made_resumes
    parser = argparse.ArgumentParser(description="Score and sort resumes.")
    parser.add_argument("--directory", type=str, required=True,
                        help="Directory with resume text files")
    args = parser.parse_args()
    main(args.directory)
