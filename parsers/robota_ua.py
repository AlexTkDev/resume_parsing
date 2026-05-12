"""Robota.ua parsers for resume listings and individual resumes."""

import json
import logging
import os
from html.parser import HTMLParser
from urllib.parse import urljoin
from typing import Any

from core.utils import clean_text, attr_value, has_classes

logger = logging.getLogger(__name__)


def _load_selectors() -> dict[str, Any]:
    """Load selectors from JSON file."""
    selectors_path = os.path.join(os.path.dirname(__file__), "selectors.json")
    with open(selectors_path, "r", encoding="utf-8") as f:
        return json.load(f)["robota_ua"]


class RobotaUaListingParser(HTMLParser):
    """Parser for robota.ua resume listing pages."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        selectors = _load_selectors()["listing"]
        self.base_url = selectors["base_url"]
        self.fields = selectors["fields"]
        self.card_tag = selectors["card_tag"]
        self.card_classes = set(selectors["card_classes"])
        self.field_selectors = selectors["selectors"]

        self.resumes: list[dict[str, Any]] = []
        self.current: dict[str, Any] | None = None
        self.card_depth = 0
        self.capture: str | None = None
        self.capture_depth = 0
        self.capture_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        if self.current is None and tag == self.card_tag and has_classes(attrs, self.card_classes):
            self.current = self.fields.copy()
            self.card_depth = 1
            return

        if self.current is None:
            return

        self.card_depth += 1

        if tag == "a" and has_classes(attrs, {"santa-no-underline"}):
            href = attr_value(attrs, "href")
            if href:
                self.current["link"] = href
        elif attr_value(attrs, "data-id") == "cv-speciality":
            self.start_capture("title")
        elif has_classes(attrs, {"santa-typo-regular", "santa-truncate"}):
            self.start_capture("name")
        elif has_classes(
            attrs,
            {"santa-flex", "santa-items-center", "santa-space-x-10", "santa-pr-20", "santa-whitespace-nowrap"},
        ):
            self.start_capture("details")
        elif has_classes(attrs, {"santa-typo-additional", "santa-text-black-500"}):
            self.start_capture("posted_time")
        elif self.capture:
            self.capture_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self.current is None:
            return

        if self.capture:
            if self.capture_depth == 0:
                text = clean_text(" ".join(self.capture_parts))
                if text:
                    self.current[self.capture] = text
                self.capture = None
                self.capture_parts = []
            else:
                self.capture_depth -= 1

        self.card_depth -= 1
        if self.card_depth == 0:
            self.resumes.append(self.current)
            self.current = None

    def handle_data(self, data: str) -> None:
        if self.capture:
            self.capture_parts.append(data)

    def start_capture(self, field: str) -> None:
        self.capture = field
        self.capture_depth = 0
        self.capture_parts = []


class RobotaUaResumeParser(HTMLParser):
    """Parser for robota.ua individual resume pages."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        selectors = _load_selectors()["resume"]
        self.section_fields = selectors["section_fields"]
        self.defaults = selectors["defaults"]
        self.field_selectors = selectors["selectors"]

        self.values: dict[str, str] = dict(self.defaults)
        self.capture: str | None = None
        self.capture_depth = 0
        self.capture_parts: list[str] = []
        self.in_section = False
        self.section_depth = 0
        self.section_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        if tag in self.section_fields and self.capture is None:
            self.start_capture(self.section_fields[tag])
            return

        if tag == "section" and not self.in_section:
            self.in_section = True
            self.section_depth = 1
            self.section_parts = []
        elif self.in_section:
            self.section_depth += 1

        if self.capture:
            self.capture_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self.capture:
            if self.capture_depth == 0:
                self.flush_capture()
            else:
                self.capture_depth -= 1

        if self.in_section:
            self.section_depth -= 1
            if self.section_depth == 0:
                text = clean_text(" ".join(self.section_parts))
                if "Додаткова інформація" in text:
                    cleaned = text.replace("Додаткова інформація", "", 1).strip()
                    self.values["additional_info"] = cleaned or self.defaults["additional_info"]
                self.in_section = False
                self.section_parts = []

    def handle_data(self, data: str) -> None:
        if self.capture:
            self.capture_parts.append(data)
        if self.in_section:
            self.section_parts.append(data)

    def start_capture(self, field: str) -> None:
        self.capture = field
        self.capture_depth = 0
        self.capture_parts = []

    def flush_capture(self) -> None:
        text = clean_text(" ".join(self.capture_parts))
        if text:
            self.values[self.capture] = text
        self.capture = None
        self.capture_parts = []

    def result(self) -> tuple[str, str]:
        """Return formatted resume data and courses."""
        resume_data = (
            f"Experience:\n{self.values['experience']}\n\n"
            f"Skills:\n{self.values['skills']}\n\n"
            f"Education:\n{self.values['education']}\n\n"
            f"Languages:\n{self.values['languages']}\n\n"
            f"Additional Information:\n{self.values['additional_info']}"
        )
        return resume_data, self.values["courses"]


def parse_robota_ua_listings(html: str) -> list[dict[str, Any]]:
    """Parse robota.ua resume listings HTML and return list of resumes."""
    parser = RobotaUaListingParser()
    parser.feed(html)
    parser.close()
    return parser.resumes


def parse_robota_ua_resume(html: str) -> tuple[str, str]:
    """Parse robota.ua individual resume HTML and return (resume_data, courses)."""
    parser = RobotaUaResumeParser()
    parser.feed(html)
    parser.close()
    return parser.result()