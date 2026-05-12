"""Tests for core utilities."""

import json
import os
import tempfile

import pytest

from core.utils import (
    load_json_list,
    save_to_json,
    clean_text,
    attr_value,
    has_classes,
    get_user_links_from_file,
    get_user_data_from_file,
    save_to_txt,
)


class TestCleanText:
    """Tests for clean_text function."""

    def test_normal_text(self) -> None:
        assert clean_text("Hello World") == "Hello World"

    def test_multiple_spaces(self) -> None:
        assert clean_text("Hello    World") == "Hello World"

    def test_newlines(self) -> None:
        assert clean_text("Hello\n\nWorld") == "Hello World"

    def test_tabs(self) -> None:
        assert clean_text("Hello\t\tWorld") == "Hello World"

    def test_mixed_whitespace(self) -> None:
        assert clean_text("  Hello   \n  World  \t  ") == "Hello World"


class TestAttrValue:
    """Tests for attr_value function."""

    def test_existing_attr(self) -> None:
        attrs = [("href", "https://example.com"), ("class", "test")]
        assert attr_value(attrs, "href") == "https://example.com"

    def test_missing_attr(self) -> None:
        attrs = [("class", "test")]
        assert attr_value(attrs, "href") == ""

    def test_default_value(self) -> None:
        attrs = [("class", "test")]
        assert attr_value(attrs, "href", "default") == "default"


class TestHasClasses:
    """Tests for has_classes function."""

    def test_has_all_classes(self) -> None:
        attrs = [("class", "card card-hover wordwrap")]
        assert has_classes(attrs, {"card", "card-hover"}) is True

    def test_missing_class(self) -> None:
        attrs = [("class", "card")]
        assert has_classes(attrs, {"card", "hover"}) is False

    def test_empty_required(self) -> None:
        attrs = [("class", "card")]
        assert has_classes(attrs, set()) is True

    def test_no_class_attr(self) -> None:
        attrs = [("href", "https://example.com")]
        assert has_classes(attrs, {"card"}) is False


class TestLoadJsonList:
    """Tests for load_json_list function."""

    def test_load_valid_json(self, sample_json_data: list[dict[str, str]]) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(sample_json_data, f)
            filepath = f.name

        try:
            result = load_json_list(filepath)
            assert result == sample_json_data
        finally:
            os.unlink(filepath)

    def test_load_empty_file(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            filepath = f.name

        try:
            result = load_json_list(filepath)
            assert result == []
        finally:
            os.unlink(filepath)

    def test_load_missing_file(self) -> None:
        result = load_json_list("/nonexistent/file.json")
        assert result == []

    def test_load_invalid_json(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            f.write("not valid json")
            filepath = f.name

        try:
            result = load_json_list(filepath)
            assert result == []
        finally:
            os.unlink(filepath)

    def test_load_non_list_json(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump({"key": "value"}, f)
            filepath = f.name

        try:
            result = load_json_list(filepath)
            assert result == []
        finally:
            os.unlink(filepath)


class TestSaveToJson:
    """Tests for save_to_json function."""

    def test_save_new_file(self, sample_json_data: list[dict[str, str]]) -> None:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            filepath = f.name

        try:
            save_to_json(sample_json_data, filepath)
            with open(filepath, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            assert loaded == sample_json_data
        finally:
            os.unlink(filepath)

    def test_merge_duplicates(self) -> None:
        existing = [{"title": "First", "link": "https://example.com/1"}]
        new = [{"title": "Second", "link": "https://example.com/1"}]

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            filepath = f.name

        try:
            json.dump(existing, open(filepath, "w", encoding="utf-8"))
            save_to_json(new, filepath)

            with open(filepath, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            assert len(loaded) == 1
            assert loaded[0]["title"] == "First"
        finally:
            os.unlink(filepath)


class TestGetUserLinksFromFile:
    """Tests for get_user_links_from_file function."""

    def test_extract_links(self) -> None:
        data = [
            {"link": "https://work.ua/resumes/123"},
            {"link": "https://work.ua/resumes/456"},
        ]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(data, f)
            filepath = f.name

        try:
            links = get_user_links_from_file(filepath)
            assert len(links) == 2
            assert "https://work.ua/resumes/123" in links
        finally:
            os.unlink(filepath)

    def test_skip_invalid_links(self) -> None:
        data = [
            {"link": "https://valid.com"},
            {"link": "No link"},
            {"title": "No link key"},
        ]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(data, f)
            filepath = f.name

        try:
            links = get_user_links_from_file(filepath)
            assert len(links) == 1
            assert links[0] == "https://valid.com"
        finally:
            os.unlink(filepath)


class TestSaveToTxt:
    """Tests for save_to_txt function."""

    def test_save_text(self) -> None:
        content = "Resume content\nLine 2"
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            filepath = f.name

        try:
            save_to_txt(content, filepath)
            with open(filepath, "r", encoding="utf-8") as f:
                loaded = f.read()
            assert loaded == content
        finally:
            os.unlink(filepath)