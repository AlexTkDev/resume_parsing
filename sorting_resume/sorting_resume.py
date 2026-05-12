"""Score and sort resumes based on relevance criteria."""

import argparse
import logging
import os
import re

from core.logging_config import setup_logging
from sorting_resume.config import CONFIG

logger = logging.getLogger(__name__)


def score_resume(resume_text: str) -> int:
    """Calculate a score for a resume based on various criteria."""
    if not resume_text.strip():
        return 0

    score = 0

    if "Experience" in resume_text or "Skills" in resume_text or "Education" in resume_text:
        for section in CONFIG["sections"]["full"]:
            if section in resume_text:
                score += CONFIG["section_weights"]["full"]
            else:
                score += CONFIG["section_weights"]["missing_penalty"]
    else:
        for section in CONFIG["sections"]["basic"]:
            if section in resume_text:
                score += CONFIG["section_weights"]["basic"]
            else:
                score += CONFIG["section_weights"]["missing_penalty"]

    for keyword in CONFIG["keywords"]:
        if keyword.lower() in resume_text.lower():
            score += CONFIG["keyword_weight"]

    experience_years = extract_experience_years(resume_text)
    for threshold in CONFIG["experience_thresholds"]:
        if experience_years >= threshold["min"]:
            score += threshold["score"]
            break

    for pattern in CONFIG["education_patterns"]:
        if re.search(rf"\b{pattern}\b", resume_text, re.IGNORECASE):
            score += CONFIG["education_weight"]
            break

    if "certificates" in resume_text.lower() or "courses" in resume_text.lower():
        cert_count = len(
            re.findall(
                rf"({"|".join(CONFIG["certificate_keywords"])})",
                resume_text,
                re.IGNORECASE,
            )
        )
        score += cert_count * CONFIG["certificate_weight"]

    logger.debug("Scored resume: %d points", score)
    return score


def extract_experience_years(resume_text: str) -> int:
    """Extract total years of experience from common English and Ukrainian forms."""
    pattern = r"(\d+)\+?\s*(?:years?|yrs?|років|роки|рік)"
    matches = re.findall(pattern, resume_text, re.IGNORECASE)

    try:
        years = sum(int(match) for match in matches)
    except ValueError:
        years = 0

    return years


def load_resumes(resume_folder: str) -> dict[str, str]:
    """Load all resume text files from a directory."""
    if not os.path.isdir(resume_folder):
        raise FileNotFoundError(f"Resume directory does not exist: {resume_folder}")

    resumes: dict[str, str] = {}
    for filename in sorted(os.listdir(resume_folder)):
        if filename.endswith(".txt"):
            filepath = os.path.join(resume_folder, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                resumes[filename] = file.read()
            logger.debug("Loaded resume: %s", filename)
    return resumes


def sort_candidates_by_relevance(resumes: dict[str, str]) -> list[tuple[str, int]]:
    """Sort resumes by their relevance score in descending order."""
    scored_resumes: dict[str, int] = {}
    for filename, text in resumes.items():
        scored_resumes[filename] = score_resume(text)

    sorted_resumes = sorted(
        scored_resumes.items(), key=lambda item: (-item[1], item[0].lower())
    )
    logger.info("Sorted %d resumes by relevance", len(sorted_resumes))
    return sorted_resumes


def main(resume_folder: str) -> None:
    """Main entry point for scoring and sorting resumes."""
    resumes = load_resumes(resume_folder)
    sorted_candidates = sort_candidates_by_relevance(resumes)

    with open("sorted_candidates.txt", "w", encoding="utf-8") as txt_file:
        for filename, score in sorted_candidates:
            resume_path = os.path.abspath(os.path.join(resume_folder, filename))
            txt_file.write(f"{filename}: {score} points\nResume path: {resume_path}\n\n")

    logger.info("Results saved to sorted_candidates.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Score and sort resumes.")
    parser.add_argument(
        "--directory",
        type=str,
        required=True,
        help="Directory with resume text files",
    )
    args = parser.parse_args()

    setup_logging()
    main(args.directory)