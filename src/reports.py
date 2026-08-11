import json
from datetime import datetime, timedelta
from functools import wraps

import pandas as pd


def save_report(filename: str = "report.json"):
    """Декоратор для сохранения результата отчёта в файл."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(result, file, ensure_ascii=False, indent=2)

            return result
        return wrapper
    return decorator


@save_report("data/weekday_report.json")
def spending_by_weekday(operations: list[dict], date: str | None = None) -> dict:
    """Считает средние траты по дням недели за последние 3 месяца."""
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    start_date = end_date - timedelta(days=90)

    df = pd.DataFrame(operations)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)
    filtered_df = df[mask]

    filtered_df = filtered_df[filtered_df["Сумма операции"] < 0]

    filtered_df["weekday"] = filtered_df["Дата операции"].dt.day_name()

    average_by_weekday = filtered_df.groupby("weekday")["Сумма операции"].mean().abs()

    result = average_by_weekday.round(2).to_dict()

    return result


if __name__ == "__main__":
    from utils import read_operations_excel

    ops = read_operations_excel("data/operations.xlsx")
    result = spending_by_weekday(ops, "2021-12-21 18:30:15")
    print(result)
