import logging
import json
import yaml
import requests
from typing import Any, Dict, Optional
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def setup_logging(level: int = logging.INFO) -> None:
    """Настроить базовое логирование."""
    logging.basicConfig(level=level, format='%(asctime)s %(levelname)s:%(message)s')


def load_json(path: str) -> Any:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Any, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_yaml(path: str) -> Dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def fetch_html(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 10) -> str:
    headers = headers or {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return ""


def setup_selenium(headless: bool = True) -> webdriver.Chrome:
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def clean_text(text: str) -> str:
    """Удаляет лишние пробелы и переносы строк."""
    return ' '.join(text.split())


def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True) 