"""Tests for work.ua and robota.ua parsers."""

import pytest

from parsers.work_ua import (
    WorkUaListingParser,
    WorkUaResumeParser,
    parse_work_ua_listings,
    parse_work_ua_resume,
)
from parsers.robota_ua import (
    RobotaUaListingParser,
    RobotaUaResumeParser,
    parse_robota_ua_listings,
    parse_robota_ua_resume,
)


class TestWorkUaListingParser:
    """Tests for Work.ua listing parser."""

    def test_parse_listing(self, work_ua_listing_html: str) -> None:
        parser = WorkUaListingParser()
        parser.feed(work_ua_listing_html)
        parser.close()

        assert len(parser.resumes) == 2

        resume = parser.resumes[0]
        assert resume["title"] == "Python Developer"
        assert resume["link"] == "https://www.work.ua/resumes/123456/"
        assert resume["name"] == "John Doe"
        assert resume["details"] == "5 years experience, Python, Django"
        assert resume["posted_time"] == "2 hours ago"

    def test_parse_empty_html(self) -> None:
        parser = WorkUaListingParser()
        parser.feed("<html><body></body></html>")
        parser.close()

        assert len(parser.resumes) == 0


class TestWorkUaResumeParser:
    """Tests for Work.ua resume parser."""

    def test_parse_resume(self, work_ua_resume_html: str) -> None:
        parser = WorkUaResumeParser()
        parser.feed(work_ua_resume_html)
        parser.close()

        result = parser.result()
        assert "Senior Python Developer" in result
        assert "John Doe" in result
        assert "Experienced software engineer" in result

    def test_parse_empty_resume(self) -> None:
        parser = WorkUaResumeParser()
        parser.feed("<html><body><p>No resume content here</p></body></html>")
        parser.close()

        result = parser.result()
        assert result == "No resume found."


class TestRobotaUaListingParser:
    """Tests for Robota.ua listing parser."""

    def test_parse_listing(self, robota_ua_listing_html: str) -> None:
        parser = RobotaUaListingParser()
        parser.feed(robota_ua_listing_html)
        parser.close()

        assert len(parser.resumes) == 2

        resume = parser.resumes[0]
        assert resume["title"] == "Full Stack Developer"
        assert resume["link"] == "/candidate/abc123"
        assert resume["name"] == "Alex Ivanov"
        assert resume["details"] == "Python, JavaScript, React"
        assert resume["posted_time"] == "2 дні тому"

    def test_parse_empty_html(self) -> None:
        parser = RobotaUaListingParser()
        parser.feed("<html><body></body></html>")
        parser.close()

        assert len(parser.resumes) == 0


class TestRobotaUaResumeParser:
    """Tests for Robota.ua resume parser."""

    def test_parse_resume(self, robota_ua_resume_html: str) -> None:
        parser = RobotaUaResumeParser()
        parser.feed(robota_ua_resume_html)
        parser.close()

        resume_data, courses = parser.result()

        assert "5 years of Python development experience" in resume_data
        assert "Django, Flask, PostgreSQL" in resume_data
        assert "Master" in resume_data
        assert "AWS Solutions Architect" in courses

    def test_parse_empty_resume(self) -> None:
        parser = RobotaUaResumeParser()
        parser.feed("<html><body></body></html>")
        parser.close()

        resume_data, courses = parser.result()
        assert "No experience information provided." in resume_data
        assert "No courses, trainings, or certificates provided." in courses


class TestWorkUaFunctions:
    """Tests for work.ua convenience functions."""

    def test_parse_work_ua_listings(self, work_ua_listing_html: str) -> None:
        result = parse_work_ua_listings(work_ua_listing_html)
        assert len(result) == 2
        assert result[0]["title"] == "Python Developer"

    def test_parse_work_ua_resume(self, work_ua_resume_html: str) -> None:
        result = parse_work_ua_resume(work_ua_resume_html)
        assert "Senior Python Developer" in result


class TestRobotaUaFunctions:
    """Tests for robota.ua convenience functions."""

    def test_parse_robota_ua_listings(self, robota_ua_listing_html: str) -> None:
        result = parse_robota_ua_listings(robota_ua_listing_html)
        assert len(result) == 2
        assert result[0]["title"] == "Full Stack Developer"

    def test_parse_robota_ua_resume(self, robota_ua_resume_html: str) -> None:
        resume_data, courses = parse_robota_ua_resume(robota_ua_resume_html)
        assert "experience" in resume_data.lower()
        assert "AWS" in courses