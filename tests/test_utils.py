from unittest.mock import Mock, patch

import pytest

from src.utils import get_currency_rates, get_greeting, get_stock_prices, read_operations_excel


@pytest.mark.parametrize("current_time, expected", [
    ("2021-01-01 08:00:00", "Доброе утро"),
    ("2021-01-01 12:00:00", "Добрый день"),
    ("2021-01-01 18:00:00", "Добрый вечер"),
    ("2021-01-01 23:00:00", "Доброй ночи"),
])
def test_get_greeting(current_time, expected):
    assert get_greeting(current_time) == expected


@pytest.fixture
def sample_operations_file(tmp_path):
    """Создаёт временный Excel-файл с тестовыми данными для теста."""
    import pandas as pd

    data = {
        "Дата операции": ["01.01.2021 10:00:00", "02.01.2021 11:00:00"],
        "Номер карты": ["*1234", "*5678"],
        "Сумма операции": [-500.0, -1000.0],
        "Категория": ["Продукты", "Транспорт"],
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "test_operations.xlsx"
    df.to_excel(file_path, index=False)

    return str(file_path)


def test_read_operations_excel(sample_operations_file):
    result = read_operations_excel(sample_operations_file)

    assert len(result) == 2
    assert result[0]["Номер карты"] == "*1234"
    assert result[1]["Сумма операции"] == -1000.0


@patch("src.utils.requests.get")
def test_get_currency_rates(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "success": True,
        "rates": {"USD": 0.0121, "EUR": 0.0105},
    }
    mock_get.return_value = mock_response

    result = get_currency_rates(["USD", "EUR"])

    assert result == [
        {"currency": "USD", "rate": round(1 / 0.0121, 2)},
        {"currency": "EUR", "rate": round(1 / 0.0105, 2)},
    ]


@patch("src.utils.time.sleep")
@patch("src.utils.requests.get")
def test_get_stock_prices(mock_get, mock_sleep):
    mock_response = Mock()
    mock_response.json.return_value = {
        "Global Quote": {"05. price": "150.25"}
    }
    mock_get.return_value = mock_response

    result = get_stock_prices(["AAPL"])

    assert result == [{"stock": "AAPL", "price": 150.25}]
