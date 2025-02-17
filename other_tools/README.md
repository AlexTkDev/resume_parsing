### Additional tool, script for getting HTML page using Selenium
**Description:**
This script is used to load the HTML content of a web page using Selenium and save it to a file. 
It is suitable for situations where you need to obtain the full HTML of a page, 
including dynamically loaded elements.

**Key Functions:**

- `get_data_by_selenium(url)`: Opens the page at the given URL using Selenium WebDriver, waits for 
all elements to load, and returns the HTML content of the page.
- `save_html_to_file(html_content, file_path)`: Saves the provided HTML content to the specified file.

**Example Execution:**

```python
    url = "https://robota.ua/candidates/all/ukraine"
    html_data = get_data_by_selenium(url)
    save_html_to_file(html_data, "page_content.html")
    print("HTML saved to 'page_content.html'")
```