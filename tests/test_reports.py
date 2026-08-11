from datetime import datetime, timedelta

import pytest

from src.reports import spending_by_weekday


@pytest.fixture
def sample_operations():
    """Тестовые транзакции на разные дни недели за последние 3 месяца."""
    today = datetime.now()

    monday = today - timedelta(days=today.weekday())
    tuesday = monday + timedelta(days=1)

    return [
        {
            "Дата операции": monday.strftime("%d.%m.%Y %H:%M:%S"),
            "Сумма операции": -1000.0,
        },
        {
            "Дата операции": monday.strftime("%d.%m.%Y %H:%M:%S"),
            "Сумма операции": -2000.0,
        },
        {
            "Дата операции": tuesday.strftime("%d.%m.%Y %H:%M:%S"),
            "Сумма операции": -500.0,
        },
    ]


def test_spending_by_weekday(sample_operations, tmp_path, monkeypatch):
    monkeypatch.setattr("src.reports.save_report", lambda filename: (lambda func: func))

    result = spending_by_weekday(sample_operations)

    assert "Monday" in result
    assert result["Monday"] == 1500.0
    assert "Tuesday" in result
    assert result["Tuesday"] == 500.0
