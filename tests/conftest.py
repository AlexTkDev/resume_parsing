"""Pytest configuration and shared fixtures."""

import pytest
from typing import Any


@pytest.fixture
def work_ua_listing_html() -> str:
    """Sample HTML for work.ua resume listing page."""
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <div class="card card-hover card-search resume-link card-visited wordwrap">
            <a href="/resumes/123456/">
                <h2>Python Developer</h2>
            </a>
            <span class="strong-600">John Doe</span>
            <p class="mb-0 overflow wordwrap">5 years experience, Python, Django</p>
            <time>2 hours ago</time>
        </div>
        <div class="card card-hover card-search resume-link card-visited wordwrap">
            <a href="/resumes/789012/">
                <h2>Backend Engineer</h2>
            </a>
            <span class="strong-600">Jane Smith</span>
            <p class="mb-0 overflow wordwrap">3 years experience, Python, Flask</p>
            <time>1 day ago</time>
        </div>
    </body>
    </html>
    """


@pytest.fixture
def work_ua_resume_html() -> str:
    """Sample HTML for work.ua individual resume page."""
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <div class="card wordwrap mt-0">
            <h2 class="mt-lg sm:mt-xl">Senior Python Developer</h2>
            <h1>John Doe</h1>
            <p>Experienced software engineer with 6 years in Python development.
            Skilled in Django, REST API, and PostgreSQL.</p>
        </div>
    </body>
    </html>
    """


@pytest.fixture
def robota_ua_listing_html() -> str:
    """Sample HTML for robota.ua resume listing page."""
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <section class="cv-card">
            <a class="santa-no-underline" href="/candidate/abc123">
                <p data-id="cv-speciality">Full Stack Developer</p>
                <p class="santa-typo-regular santa-truncate">Alex Ivanov</p>
                <div class="santa-flex santa-items-center santa-space-x-10 santa-pr-20 santa-whitespace-nowrap">
                    Python, JavaScript, React
                </div>
                <p class="santa-typo-additional santa-text-black-500">2 дні тому</p>
            </a>
        </section>
        <section class="cv-card">
            <a class="santa-no-underline" href="/candidate/def456">
                <p data-id="cv-speciality">DevOps Engineer</p>
                <p class="santa-typo-regular santa-truncate">Maria Petrenko</p>
                <div class="santa-flex santa-items-center santa-space-x-10 santa-pr-20 santa-whitespace-nowrap">
                    Docker, AWS, Kubernetes
                </div>
                <p class="santa-typo-additional santa-text-black-500">5 днів тому</p>
            </a>
        </section>
    </body>
    </html>
    """


@pytest.fixture
def robota_ua_resume_html() -> str:
    """Sample HTML for robota.ua individual resume page."""
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <alliance-shared-ui-prof-resume-experience>
            <h3>Experience</h3>
            <p>5 years of Python development experience</p>
        </alliance-shared-ui-prof-resume-experience>
        <alliance-shared-ui-prof-resume-skill-summary>
            <h3>Skills</h3>
            <p>Django, Flask, PostgreSQL, Docker, AWS</p>
        </alliance-shared-ui-prof-resume-skill-summary>
        <alliance-shared-ui-prof-resume-education>
            <h3>Education</h3>
            <p>Master's in Computer Science</p>
        </alliance-shared-ui-prof-resume-education>
        <alliance-shared-ui-prof-resume-languages>
            <h3>Languages</h3>
            <p>English - Upper Intermediate, Ukrainian - Native</p>
        </alliance-shared-ui-prof-resume-languages>
        <section>
            <p>Додаткова інформація</p>
            <p>Open to remote work</p>
        </section>
        <alliance-shared-ui-prof-resume-courses>
            <p>AWS Solutions Architect, Docker Certified Associate</p>
        </alliance-shared-ui-prof-resume-courses>
    </body>
    </html>
    """


@pytest.fixture
def sample_resume_text() -> str:
    """Sample resume text for scoring tests."""
    return """
    Experience:
    5 years of Python development with Django and Flask.

    Skills:
    Python, Django, REST API, SQL, JavaScript, Docker, AWS.

    Education:
    Master of Computer Science.

    Certificates:
    AWS Solutions Architect.
    Docker Course.
    """


@pytest.fixture
def sample_resume_minimal() -> str:
    """Minimal resume text for scoring tests."""
    return """
    Title: Junior Developer
    Name: John Doe
    Details: Looking for Python opportunities.
    """


@pytest.fixture
def empty_resume() -> str:
    """Empty resume text for scoring tests."""
    return ""


@pytest.fixture
def sample_json_data() -> list[dict[str, Any]]:
    """Sample JSON data for utils tests."""
    return [
        {"title": "Python Developer", "link": "https://work.ua/resumes/123"},
        {"title": "Backend Engineer", "link": "https://work.ua/resumes/456"},
    ]