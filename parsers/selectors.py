"""Selectors for work.ua and robota.ua parsers."""

WORK_UA = {
    "listing": {
        "card_tag": "div",
        "card_classes": ["card", "card-hover", "card-search", "resume-link", "card-visited", "wordwrap"],
        "fields": {
            "title": "No title",
            "link": "No link",
            "name": "No name",
            "details": "No details",
            "posted_time": "No time",
        },
        "selectors": {
            "link": {"tag": "a", "classes": []},
            "title": {"tag": "h2", "classes": []},
            "name": {"tag": "span", "classes": ["strong-600"]},
            "details": {"tag": "p", "classes": ["mb-0", "overflow", "wordwrap"]},
            "posted_time": {"tag": "time", "classes": []},
        },
        "base_url": "https://www.work.ua",
    },
    "resume": {
        "card_tag": "div",
        "card_classes": ["card", "wordwrap", "mt-0"],
        "fields": {
            "title": "No title",
            "name": "No name",
        },
        "selectors": {
            "title": {"tag": "h2", "classes": ["mt-lg", "sm:mt-xl"]},
            "name": {"tag": "h1", "classes": []},
        },
    },
}

ROBOTA_UA = {
    "listing": {
        "card_tag": "section",
        "card_classes": ["cv-card"],
        "fields": {
            "title": "No title",
            "link": "No link",
            "name": "No name",
            "details": "No details",
            "posted_time": "No time",
        },
        "selectors": {
            "link": {"tag": "a", "classes": ["santa-no-underline"]},
            "title": {"tag": "p", "attr": {"key": "data-id", "value": "cv-speciality"}},
            "name": {"tag": "p", "classes": ["santa-typo-regular", "santa-truncate"]},
            "details": {
                "tag": "div",
                "classes": ["santa-flex", "santa-items-center", "santa-space-x-10", "santa-pr-20", "santa-whitespace-nowrap"],
            },
            "posted_time": {"tag": "p", "classes": ["santa-typo-additional", "santa-text-black-500"]},
        },
        "base_url": "",
    },
    "resume": {
        "section_fields": {
            "alliance-shared-ui-prof-resume-experience": "experience",
            "alliance-shared-ui-prof-resume-skill-summary": "skills",
            "alliance-shared-ui-prof-resume-education": "education",
            "alliance-shared-ui-prof-resume-languages": "languages",
            "alliance-shared-ui-prof-resume-courses": "courses",
        },
        "defaults": {
            "experience": "No experience information provided.",
            "skills": "No skills information provided.",
            "education": "No education information provided.",
            "languages": "No languages information provided.",
            "additional_info": "No additional information provided.",
            "courses": "No courses, trainings, or certificates provided.",
        },
        "selectors": {
            "experience_section": {"tag": "alliance-shared-ui-prof-resume-experience", "classes": []},
            "skills_section": {"tag": "alliance-shared-ui-prof-resume-skill-summary", "classes": []},
            "education_section": {"tag": "alliance-shared-ui-prof-resume-education", "classes": []},
            "languages_section": {"tag": "alliance-shared-ui-prof-resume-languages", "classes": []},
            "courses_section": {"tag": "alliance-shared-ui-prof-resume-courses", "classes": []},
        },
    },
}
