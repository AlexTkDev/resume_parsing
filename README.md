## :technologist: Solution on Python that allows parsing and sorting of resumes from popular job websites.

## Структура папок
- work_ua/
- robota_ua/
- sorting_resume/
- ready-made_resumes/
- other_tools/
- utils/
- tests/

### :card_file_box: Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/AlexTkDev/resume_parsing.git
   cd resume_parsing
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 1. Script for Parsing Resumes from robota.ua
**Description:**
This script parses resumes from the [robota.ua](https://robota.ua) website. Selenium is used to automate the Chrome browser, which runs in headless mode (without displaying the GUI). The script iterates through resume pages and saves the data into a JSON file.

**Key Functions:**
- `setup_selenium()`: Configures the Selenium WebDriver to work with Chrome in headless mode.
- `fetch_resumes(url, driver)`: Opens the page at the given URL, locates the resume elements, and extracts information such as title, link, name, details, and publication time.
- `save_to_json(data, filename)`: Saves the data into a JSON file. If the file already exists, the data is appended to it.
- `main(pages, skill)`: The main function that manages the parsing process. It iterates through the specified pages, extracts resumes, and saves them to the `resumes_robota_ua.json` file.

**Example Execution:**
```bash
  python robota_ua/get_resume.py --pages 2 --skill python
```

---

### 2. Script for Parsing Resumes from work.ua
**Description:**
This script is designed to parse resumes from the [work.ua](https://work.ua) website using the BeautifulSoup library for HTML parsing. The script extracts resume information and saves it into a JSON file.

**Key Functions:**
- `fetch_resumes(url)`: Sends an HTTP request to the resume page and extracts information such as title, link, name, details, and publication time.
- `save_to_json(data, filename)`: Saves the data into a JSON file. If the file already exists, the data is appended to it.
- `main(pages, skill)`: The main function that iterates through the specified pages, extracts resumes, and saves them to the `resumes_work_ua.json` file.

**Example Execution:**
```bash
  python work_ua/get_resume.py --pages 2 --skill python
```

---

### 3. Script for Fetching HTML Pages Using Selenium
**Description:**
This script is used to load the HTML content of a web page using Selenium and save it to a file. It is suitable for situations where you need to obtain the full HTML of a page, including dynamically loaded elements.

**Key Functions:**
- `get_data_by_selenium(url)`: Opens the page at the given URL using Selenium WebDriver, waits for all elements to load, and returns the HTML content of the page.
- `save_html_to_file(html_content, file_path)`: Saves the provided HTML content to the specified file.

**Example Execution:**
```python
    url = "https://robota.ua/candidates/all/ukraine"
    html_data = get_data_by_selenium(url)
    save_html_to_file(html_data, "page_content.html")
    print("HTML saved to 'page_content.html'")
```

---

### 4. Script for Parsing and Saving Resumes from work.ua by Links in JSON File
**Description:**
This script extracts resume data from URLs listed in a JSON file, formats it, and saves it to 
text files. It uses the `requests` library to perform HTTP requests and `BeautifulSoup` to parse 
the HTML content of the resume pages. Each resume is saved as a `.txt` file in a designated 
directory.

**Key Functions:**
- `get_user_links(file)`: Extracts all values of the 'link' key from the provided JSON file.
- `clean_text(text)`: Cleans the text by removing unnecessary spaces and newline characters.
- `get_separate_resume(url)`: Sends an HTTP request to the resume page URL, extracts and formats the resume data such as title, name, and details.
- `save_to_txt(data, filename)`: Saves the extracted resume data to a text file.
- `main(file)`: The main function that processes each link extracted from the JSON file. It creates a directory for saving resumes (if it doesn't already exist) and saves each resume in a `.txt` file named using the user ID extracted from the URL.

**Example of running the script:**
```bash
  python work_ua/get_separate_resume.py --file resumes_work_ua.json
```

---

### 5. Script for Parsing Resumes from robota.ua Using Selenium
**Description:**
This script extracts resume data from [robota.ua](https://robota.ua) using Selenium. 
It reads candidate links and names from a JSON file, navigates to each resume page,
and extracts information such as experience, skills, education, and languages. The extracted data
is saved in a text file.

**Key Functions:**
- `setup_selenium()`: Configures the Selenium WebDriver to use Chrome in headless mode.
- `get_user_data(file)`: Extracts candidate links and names from a JSON file.
- `clean_text(text)`: Cleans text by removing unnecessary spaces and newline characters.
- `get_separate_resume(driver, url)`: Extracts resume information from the given URL using Selenium, including experience, skills, education, and languages.
- `save_to_txt(data, filename)`: Saves the extracted resume data to a text file.
- `main(file)`: The main function that processes the JSON file with candidate data, extracts resumes, and saves them to text files.

**Example of running the script:**
```bash
  python robota_ua/get_separate_resume.py --file resumes_robota_ua.json
```

**Notes:**
- The `resumes_robota_ua.json` file should contain the candidate links and names.
- The script saves the resumes in the `ready-made_resumes` directory, creating the directory 
if it doesn't exist.

---

### 6. Resume Scoring and Sorting Script
**Description:**
This script scores and sorts resumes saved in text files based on their content. 
It supports resumes from [robota.ua](https://robota.ua) and [work.ua](https://www.work.ua). 
The scoring is based on resume completeness, keywords, work experience, education, 
and additional criteria. The script sorts resumes by score in descending order and saves 
the results to a text file.

**Key Functions:**
- `score_resume(resume_text)`: Scores the resume based on its content, including resume sections, keywords, work experience, education, and additional criteria.
- `extract_experience_years(resume_text)`: Extracts the total number of years of experience from the resume text.
- `load_resumes(resume_folder)`: Loads all resumes from the specified folder.
- `sort_candidates_by_relevance(resumes)`: Sorts resumes by score in descending order based on the evaluation.
- `main(resume_folder)`: The main function that loads resumes, scores and sorts them, and then saves the results to `sorted_candidates.txt`.

**Example of running the script:**
```bash
  python sorting_resume/sorting_resume.py --directory ready-made_resumes
```

**Notes:**
- The script expects resumes to be located in the folder specified by the `--directory` argument.
- Results will be saved in `sorted_candidates.txt`, containing the resume file name, score, and path to the resume.


### 7. Collaborate
- If you have any suggestions or improvements, please feel free to contribute.
- Fork this repository.
- Create a new branch with a meaningful name.
- Open a pull request.
- Your changes will be reviewed and merged.
- Thank you for your contribution!

## Архитектура
- work_ua/ и robota_ua/ — парсеры резюме с разных сайтов
- sorting_resume/ — скрипт для оценки и сортировки резюме
- ready-made_resumes/ — папка для сохранения текстовых резюме
- other_tools/ — вспомогательные скрипты
- utils/ — общие функции и конфиги
- tests/ — модульные тесты

## Пример запуска
python work_ua/get_resume.py --pages 2 --skill python
python sorting_resume/sorting_resume.py --directory ready-made_resumes

## Тесты
pytest tests/

## Зависимости
См. requirements.txt

## Этические рекомендации
- Соблюдайте правила сайтов-источников (robots.txt, terms of use)
- Не храните чувствительные данные в репозитории

## Форматирование кода
Для автоформатирования используйте:

black .
isort .
flake8 .

## Запуск тестов
pytest tests/

## Конфиги и utils
- utils/ содержит общие функции для логирования, загрузки/сохранения, парсинга, работы с сетью и Selenium.
- config.yaml — конфигурация ключевых слов, секций, селекторов и весов для оценки резюме.

## Структура тестов
- tests/ содержит unit-тесты для всех ключевых функций (оценка, парсинг, сохранение, utils).
- Для запуска: pytest tests/

## Пример config.yaml
keywords:
  - Python
  - Django
  - REST API
  - SQL
  - JavaScript
  - Docker
  - AWS
sections:
  robota_ua:
    - Experience
    - Skills
    - Education
    - Languages
    - Additional Information
    - Courses, trainings, certificates
  work_ua:
    - Title
    - Name
    - Details
weights:
  section_found: 10
  section_missing: -2
  keyword: 5
  experience:
    more_than_5: 15
    between_3_and_5: 10
    less_than_3: 5
  education: 5
  certificate: 3

## Пример теста (tests/test_utils.py)
import pytest
from utils.utils import clean_text

def test_clean_text():
    assert clean_text('  Hello   world\n') == 'Hello world'

## pre-commit для автоматизации
- Для автоматизации форматирования и линтинга используйте pre-commit:

pre-commit install
pre-commit run --all-files

## Ручной запуск pre-commit хуков
pre-commit run --all-files

## Структура utils/
- utils/utils.py — общие функции (логирование, загрузка/сохранение, парсинг, работа с сетью и Selenium)
- utils/config.yaml — конфиг ключевых слов, секций, весов

## Best practices
- Все функции должны иметь type hints и docstrings.
- Для всех функций должны быть unit-тесты.
- Для работы с сетью и файлами всегда используйте обработку ошибок.
- Для логирования используйте logging, а не print.
- Для Selenium используйте try/finally для корректного закрытия драйвера.

## Как расширять конфиг и utils
- Для добавления новых ключевых слов, секций или весов — просто добавьте их в config.yaml.
- Для новых функций парсинга или обработки — добавьте функцию в utils/utils.py и покройте её тестом в tests/.

## Как добавить новый источник резюме
1. Добавьте парсер в новую папку (например, new_source/).
2. Опишите селекторы и секции в config.yaml.
3. Используйте функции из utils/utils.py для парсинга, логирования, сохранения.
4. Добавьте тесты для новых функций в tests/.

## Обновление зависимостей и поддержка
- Для обновления зависимостей используйте pip install -r requirements.txt
- Регулярно запускайте тесты и pre-commit хуки
- Следите за обновлениями библиотек Selenium, requests, BeautifulSoup, tqdm и др.

## Contributing
- Перед отправкой изменений убедитесь, что все тесты проходят и код отформатирован.
- Оформляйте pull request с описанием изменений и ссылкой на issue (если есть).
- Следуйте best practices и обновляйте документацию при необходимости.

## License
Проект распространяется под лицензией MIT. См. LICENSE.

## Поддержка и обратная связь
- Для вопросов и предложений создайте issue на GitHub или напишите на email, указанный в профиле автора.

## Использование как библиотеки
- Вы можете импортировать функции из utils/utils.py в свои проекты:

from utils.utils import load_config, setup_logging, fetch_html, ...

## CI/CD
- Рекомендуется настроить GitHub Actions для автоматического запуска тестов и проверки стиля при каждом pull request.
- Пример workflow см. в .github/workflows/.

## Fork и локальная разработка
- Сделайте fork репозитория на GitHub.
- Клонируйте себе: git clone ...
- Установите зависимости: pip install -r requirements.txt
- Разрабатывайте в отдельной ветке, делайте pull request в main.

## Поддержка Python и виртуальное окружение
- Рекомендуется использовать Python 3.8+
- Для изоляции зависимостей используйте venv или poetry:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Docker (опционально)
- Для удобства развертывания можно использовать Dockerfile и docker-compose.yml
- Пример Dockerfile и docker-compose.yml см. в корне репозитория (добавьте при необходимости)

## Контакты и дополнительная информация
- Для связи используйте email из профиля GitHub или создайте issue.
- Для получения дополнительной информации смотрите документацию в папке docs/ (если появится).

## Poetry (альтернатива requirements.txt)
- Для управления зависимостями можно использовать poetry:

poetry install
poetry run python ...

## Makefile (опционально)
- Для удобства можно добавить Makefile с командами для тестов, форматирования, запуска парсинга и сортировки.
- Пример:

make test
make format
make parse
make sort

## .env (опционально)
- Для хранения секретов и переменных окружения используйте .env и библиотеку python-dotenv.
- Не коммитьте .env в репозиторий (см. .gitignore)

## Ручной запуск форматирования и линтинга
- Для форматирования кода используйте:

black .
isort .
flake8 .

## Документация и примеры
- Обновляйте README.md при каждом значимом изменении.
- Примеры кода и запуска храните в папке examples/ (если потребуется).

## tqdm для прогресса
- Для отображения прогресса используйте tqdm:

from tqdm import tqdm
for page in tqdm(range(1, pages + 1)):
    ...

## Logging
- Для логирования используйте стандартный модуль logging:

import logging
logging.basicConfig(level=logging.INFO)
logging.info('Message')

## Selenium и webdriver-manager
- Для парсинга динамических страниц используйте Selenium и webdriver-manager:

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

## BeautifulSoup
- Для парсинга HTML используйте BeautifulSoup:

from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

## requests
- Для загрузки страниц используйте requests:

import requests
response = requests.get(url)
html = response.text

## pyyaml для конфигов
- Для загрузки конфигов используйте pyyaml:

import yaml
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

## json для данных
- Для сохранения и загрузки данных используйте json:

import json
with open('file.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
with open('file.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

## os и pathlib
- Для работы с файлами и путями используйте os и pathlib:

import os
from pathlib import Path

os.makedirs('dir', exist_ok=True)
file_path = Path('dir') / 'file.txt'

## argparse для CLI
- Для создания CLI используйте argparse:

import argparse
parser = argparse.ArgumentParser(description='Описание')
parser.add_argument('--param', type=str, help='Параметр')
args = parser.parse_args()

## Тестирование: unittest и pytest
- Для тестирования используйте unittest или pytest:

import pytest

def test_example():
    assert 1 + 1 == 2

## Docstrings и type hints
- Для документирования функций используйте docstrings и type hints:

def add(a: int, b: int) -> int:
    """Складывает два числа."""
    return a + b

## flake8 для проверки стиля
- Для проверки стиля используйте flake8:

flake8 .
