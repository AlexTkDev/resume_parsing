## :hammer: Project in Progress :technologist:

 
### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/AlexTkDev/resume_parsing_and_telegram_bot.git
   cd resume_parsing_and_telegram_bot
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

***

## :hammer: Проект в процессе разработки :technologist:

### Установка
1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/AlexTkDev/resume_parsing_and_telegram_bot.git
   cd resume_parsing_and_telegram_bot
   ```

2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

### 1. Скрипт для парсинга резюме с robota.ua
**Описание:**
Этот скрипт выполняет парсинг резюме с сайта [robota.ua](https://robota.ua). Используется Selenium
для автоматизации браузера Chrome, который работает в режиме без отображения GUI (headless). Скрипт
обходит страницы с резюме и сохраняет данные в JSON файл.

**Ключевые функции:**

- `setup_selenium()`: Настраивает Selenium WebDriver для работы с браузером Chrome в headless
  режиме.
- `fetch_resumes(url, driver)`: Открывает страницу по заданному URL, находит элементы с резюме и
  извлекает информацию, такую как заголовок, ссылка, имя, детали и время публикации.
- `save_to_json(data, filename)`: Сохраняет данные в JSON файл. Если файл существует, данные
  добавляются в него.
- `main(pages, skill)`: Основная функция, которая управляет процессом парсинга. Обходит указанные
  страницы, извлекает резюме и сохраняет их в файл `resumes_robota_ua.json`.

**Пример запуска:**

```bash
  python robota_ua/get_resume.py --pages 2 --skill python
```

---

### 2. Скрипт для парсинга резюме с work.ua
**Описание:**
Этот скрипт предназначен для парсинга резюме с сайта [work.ua](https://work.ua) с использованием
библиотеки BeautifulSoup для анализа HTML. Скрипт извлекает информацию о резюме и сохраняет ее в
JSON файл.

**Ключевые функции:**

- `fetch_resumes(url)`: Выполняет HTTP-запрос к странице с резюме и извлекает информацию, такую как
  заголовок, ссылка, имя, детали и время публикации.
- `save_to_json(data, filename)`: Сохраняет данные в JSON файл. Если файл существует, данные
  добавляются в него.
- `main(pages, skill)`: Основная функция, которая обходит указанные страницы, извлекает резюме и
  сохраняет их в файл `resumes_work_ua.json`.

**Пример запуска:**

```bash
  python work_ua/get_resume.py --pages 2 --skill python
```

---

### 3. Скрипт для получения HTML страницы с использованием Selenium
**Описание:**
Этот скрипт используется для загрузки HTML-кода веб-страницы с использованием Selenium и сохранения
его в файл. Подходит для ситуаций, когда нужно получить полный HTML страницы, включая динамически
загружаемые элементы.

**Ключевые функции:**

- `get_data_by_selenium(url)`: Открывает страницу по заданному URL с помощью Selenium WebDriver,
  ждет загрузки всех элементов и возвращает HTML-код страницы.
- `save_html_to_file(html_content, file_path)`: Сохраняет переданный HTML-контент в указанный файл.

**Пример запуска:**

```python
    url = "https://robota.ua/candidates/all/ukraine"
    html_data = get_data_by_selenium(url)
    save_html_to_file(html_data, "page_content.html")
    print("HTML сохранен в 'page_content.html'")
```

---

### 4. Скрипт для парсинга и сохранения резюме с work.ua по ссылкам из JSON-файла
**Описание:**
Этот скрипт извлекает данные резюме из URL, указанных в JSON-файле, форматирует их и сохраняет в 
текстовые файлы. Используются библиотеки `requests` для выполнения HTTP-запросов и `BeautifulSoup`
для анализа HTML-кода страниц резюме. Каждое резюме сохраняется в формате `.txt` 
в указанной директории.

**Ключевые функции:**
- `get_user_links(file)`: Извлекает все значения ключа 'link' из предоставленного JSON-файла.
- `clean_text(text)`: Очищает текст, удаляя лишние пробелы и символы переноса строк.
- `get_separate_resume(url)`: Отправляет HTTP-запрос к странице резюме по указанному URL, извлекает и форматирует данные резюме, такие как заголовок, имя и детали.
- `save_to_txt(data, filename)`: Сохраняет извлеченные данные резюме в текстовый файл.
- `main(file)`: Основная функция, которая обрабатывает каждую ссылку, извлеченную из JSON-файла. Создает директорию для сохранения резюме (если ее еще нет) и сохраняет каждое резюме в файл `.txt`, имя которого формируется из user ID, извлеченного из URL.

**Пример запуска:**
```bash
  python work_ua/get_separate_resume.py --file resumes_work_ua.json
```