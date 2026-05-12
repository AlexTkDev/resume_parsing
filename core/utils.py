"""Common utility functions for the project."""

import json
import logging
import os
from typing import Any


logger = logging.getLogger(__name__)


def load_json_list(filename: str) -> list[dict[str, Any]]:
    """Load a JSON file and return its contents as a list."""
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return []

    try:
        with open(filename, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        logger.warning("%s is not valid JSON. Starting with an empty list.", filename)
        return []

    if not isinstance(data, list):
        logger.warning("%s must contain a JSON list. Starting with an empty list.", filename)
        return []

    return data


def save_to_json(data: list[dict[str, Any]], filename: str) -> None:
    """Save data to a JSON file, merging with existing data to avoid duplicates."""
    existing_data = load_json_list(filename)
    unique_resumes: dict[str, dict[str, Any]] = {}

    for item in existing_data:
        link = item.get("link") if isinstance(item, dict) else None
        if link and link != "No link":
            unique_resumes[link] = item

    for item in data:
        link = item.get("link") if isinstance(item, dict) else None
        if link and link != "No link":
            if link not in unique_resumes:
                unique_resumes[link] = item

    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(list(unique_resumes.values()), json_file, ensure_ascii=False, indent=4)


def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and normalizing spaces."""
    return " ".join(text.split())


def attr_value(attrs: list[tuple[str, str]], name: str, default: str = "") -> str:
    """Get the value of an attribute from a list of attributes."""
    return dict(attrs).get(name, default)


def has_classes(attrs: list[tuple[str, str]], required: set[str]) -> bool:
    """Check if the element has all required classes."""
    if not required:
        return True
    actual_classes = set(attr_value(attrs, "class").split())
    return required.issubset(actual_classes)


def get_user_links_from_file(filepath: str) -> list[str]:
    """Extract all link values from a JSON file."""
    links: list[str] = []
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        logger.warning("No data found in %s.", filepath)
        return links

    try:
        with open(filepath, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in %s.", filepath)
        return links

    if not isinstance(data, list):
        logger.error("%s must contain a JSON list.", filepath)
        return links

    for item in data:
        if isinstance(item, dict) and item.get("link") and item["link"] != "No link":
            links.append(item["link"])

    return links


def get_user_data_from_file(filepath: str) -> list[dict[str, str]]:
    """Extract candidate links and names from a JSON file."""
    user_data: list[dict[str, str]] = []
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        logger.warning("No data found in %s.", filepath)
        return user_data

    try:
        with open(filepath, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in %s.", filepath)
        return user_data

    if not isinstance(data, list):
        logger.error("%s must contain a JSON list.", filepath)
        return user_data

    for item in data:
        if (
            isinstance(item, dict)
            and item.get("link")
            and item["link"] != "No link"
            and item.get("name")
        ):
            user_data.append({"link": item["link"], "name": item["name"]})

    return user_data


def save_to_txt(data: str, filename: str) -> None:
    """Save extracted resume data as a text file."""
    with open(filename, "w", encoding="utf-8") as txt_file:
        txt_file.write(data)