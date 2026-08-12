import pytest

from src.services import simple_search


@pytest.fixture
def sample_operations():
    """Тестовый набор транзакций для проверки поиска."""
    return [
        {"Описание": "Оплата за такси", "Категория": "Транспорт"},
        {"Описание": "Перевод другу", "Категория": "Переводы"},
        {"Описание": "Покупка продуктов", "Категория": "Супермаркеты"},
        {"Описание": None, "Категория": "Прочее"},
    ]


@pytest.mark.parametrize("query, expected_count", [
    ("такси", 1),
    ("ТАКСИ", 1),
    ("перевод", 1),
    ("несуществующий текст", 0),
])
def test_simple_search(sample_operations, query, expected_count):
    result = simple_search(sample_operations, query)
    assert len(result) == expected_count


def test_simple_search_empty_query(sample_operations):
    result = simple_search(sample_operations, "")
    assert result == []


def test_simple_search_with_invalid_data(sample_operations):
    result = simple_search(sample_operations, "прочее")
    assert len(result) == 1
    assert result[0]["Категория"] == "Прочее"


def test_simple_search_non_string_query(sample_operations):
    result = simple_search(sample_operations, None)
    assert result == []


def test_simple_search_with_non_dict_item():
    operations = [
        {"Описание": "Такси", "Категория": "Транспорт"},
        "не словарь",
        123,
    ]
    result = simple_search(operations, "такси")
    assert len(result) == 1
