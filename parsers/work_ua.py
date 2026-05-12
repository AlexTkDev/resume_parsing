"""Work.ua parsers for resume listings and individual resumes."""

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
        return json.load(f)["work_ua"]


class WorkUaListingParser(HTMLParser):
    """Parser for work.ua resume listing pages."""

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

        if tag == "a" and self.current["link"] == "No link":
            href = attr_value(attrs, "href")
            if href:
                self.current["link"] = urljoin(self.base_url, href)

        if tag == "h2":
            self.start_capture("title")
        elif tag == "span" and has_classes(attrs, {"strong-600"}):
            self.start_capture("name")
        elif tag == "p" and has_classes(attrs, {"mb-0", "overflow", "wordwrap"}):
            self.start_capture("details")
        elif tag == "time":
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


class WorkUaResumeParser(HTMLParser):
    """Parser for work.ua individual resume pages."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        selectors = _load_selectors()["resume"]
        self.card_tag = selectors["card_tag"]
        self.card_classes = set(selectors["card_classes"])
        self.fields = selectors["fields"]

        self.in_resume = False
        self.resume_depth = 0
        self.resume_parts: list[str] = []
        self.title = "No title"
        self.name = "No name"
        self.capture: str | None = None
        self.capture_depth = 0
        self.capture_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        resume_classes = {"card", "wordwrap", "mt-0"}
        if not self.in_resume and tag == self.card_tag and has_classes(attrs, resume_classes):
            self.in_resume = True
            self.resume_depth = 1
            return

        if not self.in_resume:
            return

        self.resume_depth += 1

        if tag == "h2" and has_classes(attrs, {"mt-lg", "sm:mt-xl"}):
            self.start_capture("title")
        elif tag == "h1":
            self.start_capture("name")
        elif self.capture:
            self.capture_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if not self.in_resume:
            return

        if self.capture:
            if self.capture_depth == 0:
                text = clean_text(" ".join(self.capture_parts))
                if text:
                    setattr(self, self.capture, text)
                self.capture = None
                self.capture_parts = []
            else:
                self.capture_depth -= 1

        self.resume_depth -= 1
        if self.resume_depth == 0:
            self.in_resume = False

    def handle_data(self, data: str) -> None:
        if self.in_resume:
            self.resume_parts.append(data)
        if self.capture:
            self.capture_parts.append(data)

    def start_capture(self, field: str) -> None:
        self.capture = field
        self.capture_depth = 0
        self.capture_parts = []

    def result(self) -> str:
        details = clean_text(" ".join(self.resume_parts)) if self.resume_parts else "No details"
        if details == "No details":
            return "No resume found."
        return f"Title: {self.title}\nName: {self.name}\nDetails: {details}\n"


def parse_work_ua_listings(html: str) -> list[dict[str, Any]]:
    """Parse work.ua resume listings HTML and return list of resumes."""
    parser = WorkUaListingParser()
    parser.feed(html)
    parser.close()
    return parser.resumes


def parse_work_ua_resume(html: str) -> str:
    """Parse work.ua individual resume HTML and return formatted resume."""
    parser = WorkUaResumeParser()
    parser.feed(html)
    parser.close()
    return parser.result()