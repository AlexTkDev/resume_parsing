"""Tests for resume scoring and sorting."""

import pytest

from sorting_resume.sorting_resume import (
    score_resume,
    extract_experience_years,
    sort_candidates_by_relevance,
)


class TestScoreResume:
    """Tests for resume scoring function."""

    def test_full_resume_high_score(self, sample_resume_text: str) -> None:
        score = score_resume(sample_resume_text)
        assert score > 30

    def test_minimal_resume_lower_score(self, sample_resume_minimal: str) -> None:
        score = score_resume(sample_resume_minimal)
        assert score < 30

    def test_empty_resume(self, empty_resume: str) -> None:
        score = score_resume(empty_resume)
        assert score == 0

    def test_python_keyword(self) -> None:
        text = "Python developer with Django experience"
        score = score_resume(text)
        assert score >= 5

    def test_multiple_keywords(self) -> None:
        text = "Experience: 3 years\nSkills: Python, Django, REST API, SQL, JavaScript, Docker, AWS"
        score = score_resume(text)
        keyword_points = 7 * 5
        assert score >= keyword_points

    def test_education_boost(self) -> None:
        text = "Experience: 2 years\nSkills: Python\nEducation: Master of Computer Science"
        score = score_resume(text)
        assert score >= 5

    def test_certificate_boost(self) -> None:
        text = "Certificate: AWS Solutions Architect. Course: Docker Fundamentals"
        score = score_resume(text)
        assert score >= 6


class TestExtractExperienceYears:
    """Tests for experience extraction."""

    def test_english_years(self) -> None:
        text = "5 years of experience in Python development"
        years = extract_experience_years(text)
        assert years == 5

    def test_ukrainian_років(self) -> None:
        text = "Маю 3 роки досвіду у Python"
        years = extract_experience_years(text)
        assert years == 3

    def test_ukrainian_роки(self) -> None:
        text = "1 рік досвіду"
        years = extract_experience_years(text)
        assert years == 1

    def test_multiple_mentions(self) -> None:
        text = "5 years in backend, 2 years in frontend"
        years = extract_experience_years(text)
        assert years == 7

    def test_plus_years(self) -> None:
        text = "10+ years of senior experience"
        years = extract_experience_years(text)
        assert years == 10

    def test_no_experience(self) -> None:
        text = "No experience mentioned"
        years = extract_experience_years(text)
        assert years == 0

    def test_empty_text(self) -> None:
        years = extract_experience_years("")
        assert years == 0


class TestSortCandidatesByRelevance:
    """Tests for sorting resumes by relevance."""

    def test_sort_by_score(self) -> None:
        resumes = {
            "low_score.txt": "Title: Junior Dev\nName: John\nDetails: Basic",
            "high_score.txt": (
                "Experience:\n5 years\nSkills:\nPython, Django\nEducation:\nMaster\n"
            ),
        }
        sorted_resumes = sort_candidates_by_relevance(resumes)

        assert sorted_resumes[0][0] == "high_score.txt"
        assert sorted_resumes[0][1] > sorted_resumes[1][1]

    def test_sort_alphabetically_when_equal_score(self) -> None:
        resumes = {
            "z_resume.txt": "Title: Dev\nName: Z\nDetails: Test",
            "a_resume.txt": "Title: Dev\nName: A\nDetails: Test",
        }
        sorted_resumes = sort_candidates_by_relevance(resumes)

        assert sorted_resumes[0][0] == "a_resume.txt"
        assert sorted_resumes[1][0] == "z_resume.txt"
        assert sorted_resumes[0][1] == sorted_resumes[1][1]

    def test_empty_dict(self) -> None:
        sorted_resumes = sort_candidates_by_relevance({})
        assert sorted_resumes == []