"""Base parser classes for HTML parsing."""

from abc import ABC, abstractmethod
from html.parser import HTMLParser
from typing import Any


class BaseListingParser(HTMLParser, ABC):
    """Abstract base class for resume listing parsers."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.resumes: list[dict[str, Any]] = []
        self.current: dict[str, Any] | None = None
        self.card_depth = 0
        self.capture: str | None = None
        self.capture_depth = 0
        self.capture_parts: list[str] = []

    @abstractmethod
    def get_card_tag(self) -> str:
        """Return the HTML tag that identifies a card element."""
        pass

    @abstractmethod
    def get_card_classes(self) -> set[str]:
        """Return the CSS classes that identify a card element."""
        pass

    @abstractmethod
    def get_card_fields(self) -> dict[str, Any]:
        """Return the default fields for a card."""
        pass

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        from core.utils import has_classes

        if self.current is None and tag == self.get_card_tag() and has_classes(
            attrs, self.get_card_classes()
        ):
            self.current = self.get_card_fields()
            self.card_depth = 1
            return

        if self.current is None:
            return

        self.card_depth += 1
        self._handle_card_starttag(tag, attrs)

        if self.capture:
            self.capture_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self.current is None:
            return

        if self.capture:
            if self.capture_depth == 0:
                from core.utils import clean_text

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

    @abstractmethod
    def _handle_card_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        """Handle start tags within a card element. Implement in subclass."""
        pass

    def parse(self, html: str) -> list[dict[str, Any]]:
        """Parse HTML and return list of resumes."""
        self.feed(html)
        self.close()
        return self.resumes