from src .reports import spending_by_weekday
from src .services import simple_search
from src .utils import read_operations_excel
from src .views import main_page

if __name__ == '__main__':
    # Веб-страница «Главная»
    print(main_page("2021-12-21 18:30:15"))

    # Сервис «Простой поиск»
    operations = read_operations_excel("data/operations.xlsx")
    found = simple_search(operations, "перевод")
    print(f"Найдено операций: {len(found)}")

    # Отчёт «Траты по дням недели»
    report = spending_by_weekday(operations, "2021-12-21 18:30:15")
    print(report)
