# Resume Parser

Collects resumes from work.ua and robota.ua, exports candidate profiles, and ranks them by relevance.

## Features

- Parses resume listings from both platforms
- Exports individual resumes to text files
- Ranks candidates by skills, experience, education
- Uses requests for work.ua and Selenium for robota.ua
- Configurable via environment variables

## Quick Start

```bash
git clone https://github.com/AlexTkDev/resume_parsing.git
cd resume_parsing
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Settings are stored in `.env` (copy from `.env.example`).

## Usage

**Collect listings:**
```bash
python work_ua/get_resume.py --pages 2 --skill python
python robota_ua/get_resume.py --pages 2 --skill python
```

**Export resumes:**
```bash
python work_ua/get_separate_resume.py --file resumes_work_ua.json
python robota_ua/get_separate_resume.py --file resumes_robota_ua.json
```

**Rank candidates:**
```bash
python sorting_resume/sorting_resume.py --directory ready-made_resumes
```

## Project Structure

| Folder | Purpose |
|--------|---------|
| `core/` | Shared utilities: HTTP, Selenium, logging |
| `parsers/` | Parsers with JSON selectors |
| `work_ua/` | work.ua scripts |
| `robota_ua/` | robota.ua scripts (Selenium) |
| `sorting_resume/` | Relevance scoring |
| `tests/` | Unit tests |

## Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `REQUEST_TIMEOUT` | 10 | HTTP request timeout, sec |
| `SLEEP_MIN` | 5 | Min delay between requests |
| `SLEEP_MAX` | 20 | Max delay between requests |
| `HEADLESS` | true | Run Chrome without GUI |
| `LOG_LEVEL` | INFO | Logging level |

## Tests

```bash
pytest
```

## Note

Parsers use selectors from `parsers/selectors.json`. If sites change their layout, update the selectors in this file.
