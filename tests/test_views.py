from unittest.mock import mock_open, patch

import pytest

from src.views import filter_by_month, get_cards_info, get_top_transactions, main_page


@pytest.fixture
def sample_operations():
    """Тестовые транзакции для декабря 2021."""
    return [
        {
            "Дата операции": "05.12.2021 10:00:00",
            "Дата платежа": "05.12.2021",
            "Номер карты": "*1234",
            "Сумма операции": -1000.0,
            "Категория": "Продукты",
            "Описание": "Пятёрочка",
        },
        {
            "Дата операции": "10.12.2021 12:00:00",
            "Дата платежа": "10.12.2021",
            "Номер карты": "*1234",
            "Сумма операции": -5000.0,
            "Категория": "Транспорт",
            "Описание": "Такси",
        },
        {
            "Дата операции": "15.11.2021 09:00:00",
            "Дата платежа": "15.11.2021",
            "Номер карты": "*5678",
            "Сумма операции": -2000.0,
            "Категория": "Развлечения",
            "Описание": "Кино",
        },
        {
            "Дата операции": "20.12.2021 14:00:00",
            "Дата платежа": "20.12.2021",
            "Номер карты": float("nan"),
            "Сумма операции": -300.0,
            "Категория": "Прочее",
            "Описание": "Мелочи",
        },
    ]


def test_filter_by_month(sample_operations):
    result = filter_by_month(sample_operations, "2021-12-21 18:30:15")

    assert len(result) == 3
    assert all("12.2021" in op["Дата операции"] for op in result)


def test_filter_by_month_with_invalid_date():
    operations = [
        {"Дата операции": float("nan")},
        {"Дата операции": "05.12.2021 10:00:00"},
    ]
    result = filter_by_month(operations, "2021-12-21 18:30:15")
    assert len(result) == 1


def test_get_cards_info(sample_operations):
    filtered = [op for op in sample_operations if op["Номер карты"] == "*1234"]
    result = get_cards_info(filtered)

    assert len(result) == 1
    assert result[0]["last_digits"] == "1234"
    assert result[0]["total_spend"] == 6000.0
    assert result[0]["cashback"] == 60.0


def test_get_cards_info_with_invalid_amount():
    operations = [
        {"Номер карты": "*1234", "Сумма операции": float("nan")},
        {"Номер карты": "*1234", "Сумма операции": 500.0},
        {"Номер карты": "*1234", "Сумма операции": -1000.0},
    ]
    result = get_cards_info(operations)
    assert len(result) == 1
    assert result[0]["total_spend"] == 1000.0


def test_get_top_transactions(sample_operations):
    result = get_top_transactions(sample_operations)

    assert len(result) == 4
    assert result[0]["amount"] == -5000.0


def test_get_top_transactions_with_invalid_amount():
    operations = [
        {
            "Сумма операции": float("nan"),
            "Дата платежа": "01.01.2021",
            "Категория": "A",
            "Описание": "a",
        },
        {"Сумма операции": -500.0, "Дата платежа": "02.01.2021", "Категория": "B", "Описание": "b"},
    ]
    result = get_top_transactions(operations)
    assert len(result) == 1


@patch("src.views.get_stock_prices")
@patch("src.views.get_currency_rates")
@patch("src.views.read_operations_excel")
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"user_currencies": ["USD"], "user_stocks": ["AAPL"]}',
)
def test_main_page(mock_file, mock_read_excel, mock_currency_rates, mock_stock_prices):
    mock_read_excel.return_value = [
        {
            "Дата операции": "05.12.2021 10:00:00",
            "Дата платежа": "05.12.2021",
            "Номер карты": "*1234",
            "Сумма операции": -1000.0,
            "Категория": "Продукты",
            "Описание": "Пятёрочка",
        }
    ]
    mock_currency_rates.return_value = [{"currency": "USD", "rate": 90.0}]
    mock_stock_prices.return_value = [{"stock": "AAPL", "price": 150.0}]

    result = main_page("2021-12-21 18:30:15")

    assert "Добрый вечер" in result
    assert "1234" in result
    assert "AAPL" in result
