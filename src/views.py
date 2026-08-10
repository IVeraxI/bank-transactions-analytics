import json
from datetime import datetime
from utils import get_currency_rates, get_greeting, get_stock_prices, read_operations_excel


def filter_by_month(operations: list[dict], datetime_str: str) -> list[dict]:
    """Фильтрует операции с начала месяца до указанной даты."""
    end_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    start_date = end_date.replace(day=1, hour=0, minute=0, second=0)

    filtered = []
    for operation in operations:
        operation_date_str = operation.get("Дата операции")
        if not isinstance(operation_date_str, str):
            continue

        operation_date = datetime.strptime(operation_date_str, "%d.%m.%Y %H:%M:%S")

        if start_date <= operation_date <= end_date:
            filtered.append(operation)

    return filtered


def get_cards_info(operations: list[dict]) -> list[dict]:
    """Считает сумму трат и кэшбэк по каждой карте."""
    cards: dict[str, float] = {}

    for operation in operations:
        card_number = operation.get("Номер карты")
        amount = operation.get("Сумма операции")

        if not isinstance(card_number, str) or not isinstance(amount, (int, float)):
            continue

        if amount >= 0:
            continue

        last_digits = card_number[-4:]
        cards[last_digits] = cards.get(last_digits, 0) + abs(amount)

    result = []
    for last_digits, total_spend in cards.items():
        result.append({
            "last_digits": last_digits,
            "total_spend": round(total_spend, 2),
            "cashback": round(total_spend / 100, 2),
        })

    return result


def get_top_transactions(operations: list[dict]) -> list[dict]:
    """Возвращает топ-5 транзакций по сумме платежа."""
    valid_operations = []
    for operation in operations:
        amount = operation.get("Сумма операции")
        if isinstance(amount, (int, float)):
            valid_operations.append(operation)

    sorted_operations = sorted(valid_operations, key=lambda op: abs(op["Сумма операции"]), reverse=True)
    top_5 = sorted_operations[:5]

    result = []
    for operation in top_5:
        result.append({
            "date": operation.get("Дата платежа"),
            "amount": operation.get("Сумма операции"),
            "category": operation.get("Категория"),
            "description": operation.get("Описание")
        })

    return result


def main_page(datetime_str: str) -> str:
    """Формирует данные для главной страницы в формате JSON."""
    with open("user_settings.json", "r", encoding="utf-8") as file:
        settings = json.load(file)

    operations = read_operations_excel("data/operations.xlsx")
    filtered_operations = filter_by_month(operations, datetime_str)

    response = {
        "greeting": get_greeting(datetime_str),
        "cards": get_cards_info(filtered_operations),
        "top_transactions": get_top_transactions(filtered_operations),
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"]),
    }

    return json.dumps(response, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    result = main_page("2021-12-21 18:30:15")
    print(result)