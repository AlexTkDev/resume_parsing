from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Настройка Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Работать в фоновом режиме без GUI


def get_data_by_selenium(url: str) -> str:
    """Звертається до сервера за url адресою і повертає HTML сайту"""
    service = ChromeService(ChromeDriverManager().install())
    with webdriver.Chrome(service=service, options=chrome_options) as driver:
        driver.get(url)
        print(f"Страница загружена: {driver.title}")  # Вывести заголовок страницы
        try:
            # Дождаться загрузки HTML
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            data = driver.page_source
        except Exception as e:
            print(f"Ошибка: {e}")
            data = driver.page_source  # Вернуть HTML даже если есть ошибка
    return data


def save_html_to_file(html_content: str, file_path: str):
    """Сохраняет HTML контент в файл"""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)


url = "https://robota.ua/candidates/all/ukraine"
html_data = get_data_by_selenium(url)
save_html_to_file(html_data, "page_content.html")
print("HTML сохранен в 'page_content.html'")
