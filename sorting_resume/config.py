"""Scoring configuration."""

CONFIG = {
    "sections": {
        "full": ["Experience", "Skills", "Education", "Languages", "Additional Information", "Courses, trainings, certificates"],
        "basic": ["Title", "Name", "Details"],
    },
    "section_weights": {
        "full": 10,
        "basic": 5,
        "missing_penalty": -2,
    },
    "keywords": ["Python", "Django", "REST API", "SQL", "JavaScript", "Docker", "AWS"],
    "keyword_weight": 5,
    "experience_thresholds": [
        {"min": 5, "score": 15},
        {"min": 3, "score": 10},
        {"min": 0, "score": 5},
    ],
    "education_patterns": ["Bachelor", "Master", "MCA", "BCA", "Computer Science", "Engineering"],
    "education_weight": 5,
    "certificate_weight": 3,
    "certificate_keywords": ["certificate", "course"],
}
