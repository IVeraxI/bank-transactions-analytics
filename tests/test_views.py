import pytest

from src.views import filter_by_month, get_cards_info, get_top_transactions


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


def test_get_cards_info(sample_operations):
    filtered = [op for op in sample_operations if op["Номер карты"] == "*1234"]
    result = get_cards_info(filtered)

    assert len(result) == 1
    assert result[0]["last_digits"] == "1234"
    assert result[0]["total_spend"] == 6000.0
    assert result[0]["cashback"] == 60.0


def test_get_top_transactions(sample_operations):
    result = get_top_transactions(sample_operations)

    assert len(result) == 4
    assert result[0]["amount"] == -5000.0
