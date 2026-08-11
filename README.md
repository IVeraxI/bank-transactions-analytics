# Bank Transactions Analytics

Приложение для анализа банковских операций. Курсовая работа по модулю 3 курса Python-разработки SkyPro.

Приложение читает данные о транзакциях из Excel-файла и предоставляет:

- **Веб-страницу «Главная»** — приветствие, сводку по картам, топ-5 транзакций, курсы валют и цены акций в формате JSON
- **Сервис «Простой поиск»** — поиск транзакций по подстроке в описании или категории
- **Отчёт «Траты по дням недели»** — среднюю сумму трат по каждому дню недели за последние 3 месяца

## Стек

- Python 3.14
- pandas — обработка табличных данных и агрегация
- requests — обращение к внешним API
- python-dotenv — хранение секретных ключей
- openpyxl — чтение Excel-файлов
- pytest, pytest-cov — тестирование и покрытие кода
- flake8, mypy, black, isort — линтеры и форматирование

## Установка

```bash
git clone https://github.com/IVeraxI/bank-transactions-analytics.git
cd bank-transactions-analytics
poetry install
```

Скопируй `.env_template` в `.env` и укажи свои ключи:

```
API_KEY_APILAYER=your_api_key_here
API_KEY_ALPHAVANTAGE=your_api_key_here
```

- Ключ APILayer — https://apilayer.com/ (Exchange Rates Data API, Free план)
- Ключ Alpha Vantage — https://www.alphavantage.co/support/#api-key

Положи файл с транзакциями в `data/operations.xlsx`.

## Использование

```bash
python src/views.py
```

Выведет JSON с данными для главной страницы.

## Тестирование

Для запуска тестов используется библиотека `pytest`.

### Запуск тестов

```bash
pytest tests/ -v
```

### Запуск с отчётом покрытия

```bash
pytest --cov=src --cov-report=html --cov-report=term -v
```

Отчёт покрытия в HTML-формате сохраняется в папку `htmlcov/`.

### Покрытие кода

Покрытие тестами составляет более 90%. В тестах используются фикстуры для генерации тестовых данных, параметризация для проверки разных входных случаев, и mock для изоляции тестов от реальных обращений к внешним API.

## Структура проекта

```
bank-transactions-analytics/
├── src/
│   ├── utils.py       # чтение данных, приветствие, внешние API
│   ├── views.py       # логика главной страницы
│   ├── services.py    # сервис простого поиска
│   └── reports.py     # отчёт по дням недели
├── data/
│   └── operations.xlsx
├── tests/
│   ├── test_utils.py
│   ├── test_views.py
│   ├── test_services.py
│   └── test_reports.py
└── user_settings.json # настройки валют и акций для главной страницы
```