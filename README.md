## :technologist: Solution on Python that allows parsing and sorting of resumes from popular job websites.

 
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

