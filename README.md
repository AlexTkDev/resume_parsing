# Resume Parser

Собирает резюме с work.ua и robota.ua, экспортирует профили кандидатов и ранжирует их по релевантности.

## Что умеет

- Парсит листинги резюме с двух платформ
- Экспортирует отдельные резюме в текстовые файлы
- Ранжирует кандидатов по ключевым навыкам, опыту, образованию
- Работает через requests (work.ua) и Selenium (robota.ua)
- Настраивается через переменные окружения

## Быстрый старт

```bash
git clone https://github.com/AlexTkDev/resume_parsing.git
cd resume_parsing
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Настройки хранятся в `.env` (скопируйте из `.env.example`).

## Использование

**Собрать листинги:**
```bash
python work_ua/get_resume.py --pages 2 --skill python
python robota_ua/get_resume.py --pages 2 --skill python
```

**Экспортировать резюме:**
```bash
python work_ua/get_separate_resume.py --file resumes_work_ua.json
python robota_ua/get_separate_resume.py --file resumes_robota_ua.json
```

**Ранжировать кандидатов:**
```bash
python sorting_resume/sorting_resume.py --directory ready-made_resumes
```

## Структура проекта

| Папка | Назначение |
|-------|------------|
| `core/` | Общие утилиты: HTTP, Selenium, логирование |
| `parsers/` | Парсеры с селекторами в JSON |
| `work_ua/` | Скрипты для work.ua |
| `robota_ua/` | Скрипты для robota.ua (Selenium) |
| `sorting_resume/` | Подсчёт релевантности |
| `tests/` | Тесты |

## Настройки

| Переменная | По умолчанию | Описание |
|------------|--------------|----------|
| `REQUEST_TIMEOUT` | 10 | Таймаут HTTP-запросов, сек |
| `SLEEP_MIN` | 5 | Минимальная задержка между запросами |
| `SLEEP_MAX` | 20 | Максимальная задержка между запросами |
| `HEADLESS` | true | Запуск Chrome без GUI |
| `LOG_LEVEL` | INFO | Уровень логирования |

## Тесты

```bash
pytest
```

## Примечание

Парсеры используют селекторы из `parsers/selectors.json`. Если сайты изменят вёрстку — обновите селекторы в этом файле.
