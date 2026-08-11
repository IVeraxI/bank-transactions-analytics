def simple_search(operations: list[dict], search_string: str) -> list[dict]:
    """Ищет операции, где строка встречается в описании или категории."""
    if not isinstance(search_string, str) or not search_string.strip():
        return []

    query = search_string.lower()
    result = []

    for op in operations:
        if not isinstance(op, dict):
            continue

        description = op.get("Описание")
        category = op.get("Категория")

        in_description = isinstance(description, str) and query in description.lower()
        in_category = isinstance(category, str) and query in category.lower()

        if in_description or in_category:
            result.append(op)

    return result


if __name__ == "__main__":
    from utils import read_operations_excel

    ops = read_operations_excel("data/operations.xlsx")
    found = simple_search(ops, "перевод")
    print(len(found))
    print(found[:2])