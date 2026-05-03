# Resume Parsing and Candidate Ranking

Production-ready Python scripts for collecting resumes from Ukrainian job platforms,
exporting candidate profiles, and ranking resumes by relevance.

Developed by AlexTkDev for a client project delivered through
[ForgeFlow Tech](https://www.upwork.com/agencies/2050880168568328242/).

## Overview

The project automates a simple recruitment workflow:

1. Collect resume listings from `work.ua` and `robota.ua`.
2. Save listing metadata to JSON files.
3. Open each candidate profile and export the resume to a text file.
4. Score exported resumes by completeness, keywords, experience, education, and courses.
5. Save a ranked candidate list for review.

## Parsing Approach

HTML extraction is implemented with an incremental parser based on Python's standard
`html.parser.HTMLParser`.

This follows the same practical direction described in Cloudflare's HTML parsing article:
parse HTML as a stream of tokens, extract only matching elements, and avoid building a full
browser-style DOM when it is not needed.

Implementation details:

- `work.ua` pages are fetched with `requests` and parsed with streaming extractors.
- `robota.ua` pages are rendered with Selenium because content is dynamic, then parsed from
  `driver.page_source` with streaming extractors.
- BeautifulSoup/DOM-based parsing is not used in the production extraction path.
- Extractors are local to each source:
  - `work_ua/html_stream_parser.py`
  - `robota_ua/html_stream_parser.py`

## Features

- Resume listing parsing for `work.ua` and `robota.ua`.
- Separate resume export to `.txt`.
- JSON output with deduplication by candidate link.
- Candidate ranking by profile completeness, keywords, experience, education, and courses.
- HTTP timeout, status validation, browser-like headers, and safe JSON handling.
- Selenium driver cleanup with `try/finally`.
- HTML debug export utility for dynamic pages.

## Requirements

- Python 3.12+
- Google Chrome for Selenium-based `robota.ua` scripts
- Internet access to target websites

Install dependencies:

```bash
git clone https://github.com/AlexTkDev/resume_parsing.git
cd resume_parsing
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

For Windows:

```bash
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Collect resume listings:

```bash
python work_ua/get_resume.py --pages 2 --skill python
python robota_ua/get_resume.py --pages 2 --skill python
```

If `--skill` is omitted, scripts collect general resume listings.

Export separate resume files:

```bash
python work_ua/get_separate_resume.py --file resumes_work_ua.json
python robota_ua/get_separate_resume.py --file resumes_robota_ua.json
```

Rank exported resumes:

```bash
python sorting_resume/sorting_resume.py --directory ready-made_resumes
```

Save rendered HTML for selector debugging:

```bash
python other_tools/get_all_html.py \
  "https://robota.ua/candidates/all/ukraine" \
  --output page_content.html
```

## Outputs

- `resumes_work_ua.json` - parsed listing metadata from `work.ua`.
- `resumes_robota_ua.json` - parsed listing metadata from `robota.ua`.
- `ready-made_resumes/` - exported candidate profiles as `.txt` files.
- `sorted_candidates.txt` - ranked candidates with score and local resume path.

Generated JSON, TXT, HTML, and exported resume files are ignored by Git.

## Project Structure

```text
work_ua/
  get_resume.py             # Collect work.ua resume listings
  get_separate_resume.py    # Export work.ua resumes by JSON links
  html_stream_parser.py     # work.ua streaming HTML extractors

robota_ua/
  get_resume.py             # Collect robota.ua resume listings through Selenium
  get_separate_resume.py    # Export robota.ua resumes by JSON links
  html_stream_parser.py     # robota.ua streaming HTML extractors

sorting_resume/
  sorting_resume.py         # Score and rank exported resumes

other_tools/
  get_all_html.py           # Save rendered HTML for debugging selectors
```

## Operational Notes

- Target websites can change markup or access policies. If parsing returns no results, refresh
  selectors in the corresponding `html_stream_parser.py`.
- `robota.ua` requires Selenium rendering because the page content is dynamic.
- Random delays are used between listing page requests to reduce request bursts.
- The scoring logic is deterministic and intentionally lightweight; it is designed for shortlist
  support, not automated hiring decisions.

## Validation

Recommended checks before delivery:

```bash
python -m compileall -q .
python -m flake8
python sorting_resume/sorting_resume.py --directory ready-made_resumes
```

Run live parser checks only when network access and target site availability are confirmed.
