### Rendered HTML export

Utility script for saving a Selenium-rendered page to an HTML file. Useful when a target page
loads content dynamically and raw `requests` output is not enough for debugging selectors.

```bash
python other_tools/get_all_html.py \
  "https://robota.ua/candidates/all/ukraine" \
  --output page_content.html
```

The default output file is `page_content.html`.
