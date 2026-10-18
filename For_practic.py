
import csv
import os

FILE_NAME = "employees.csv"

FIELDS = [
    "Имя",
    "Фамилия",
    "Возраст",
    "Должность",
    "Оклад",
    "Отдел",
]


def add_employee(employees):
    """Добавление нового сотрудника."""
    try:
        name = input("Введите имя: ").strip()
        surname = input("Введите фамилию: ").strip()
        age = int(input("Введите возраст: "))
        position = input("Введите должность: ").strip()
        salary = float(input("Введите оклад: "))
        department = input("Введите отдел: ").strip()

        if not name or not surname or not position or not department:
            raise ValueError("Текстовые поля не должны быть пустыми.")
        if age <= 0 or salary < 0:
            raise ValueError(
                "Возраст должен быть положительным, "
                "а оклад не может быть отрицательным."
            )

        employee = {
            "Имя": name,
            "Фамилия": surname,
            "Возраст": age,
            "Должность": position,
            "Оклад": salary,
            "Отдел": department,
        }
        employees.append(employee)
        print("Сотрудник успешно добавлен.")
    except ValueError as error:
        print("Ошибка ввода:", error)


def show_employees(employees):
    """Вывод списка сотрудников."""
    if not employees:
        print("Список сотрудников пуст.")
        return

    for number, employee in enumerate(employees, start=1):
        print(f"\nСотрудник №{number}")
        for field in FIELDS:
            print(f"{field}: {employee[field]}")


def delete_employee(employees):
    """Удаление сотрудника по номеру."""
    show_employees(employees)
    if not employees:
        return
    try:
        number = int(input("\nВведите номер сотрудника для удаления: "))
        if number < 1 or number > len(employees):
            raise ValueError("Сотрудника с таким номером нет.")
        deleted = employees.pop(number - 1)
        print(
            f"Сотрудник {deleted['Имя']} {deleted['Фамилия']} удалён."
        )
    except ValueError as error:
        print("Ошибка:", error)


def sort_employees(employees):
    """Сортировка по возрасту или окладу."""
    print("1. Сортировка по возрасту")
    print("2. Сортировка по окладу")
    choice = input("Выберите способ сортировки: ")
    if choice == "1":
        employees.sort(key=lambda employee: employee["Возраст"])
        print("Сотрудники отсортированы по возрасту.")
    elif choice == "2":
        employees.sort(key=lambda employee: employee["Оклад"])
        print("Сотрудники отсортированы по окладу.")
    else:
        print("Неверный пункт меню.")
        return
    show_employees(employees)


def filter_employees(employees):
    """Фильтрация по должности или отделу."""
    print("1. Фильтрация по должности")
    print("2. Фильтрация по отделу")
    choice = input("Выберите способ фильтрации: ")
    if choice == "1":
        value = input("Введите должность: ").strip().casefold()
        result = [
            employee
            for employee in employees
            if employee["Должность"].casefold() == value
        ]
    elif choice == "2":
        value = input("Введите отдел: ").strip().casefold()
        result = [
            employee
            for employee in employees
            if employee["Отдел"].casefold() == value
        ]
    else:
        print("Неверный пункт меню.")
        return

    if result:
        show_employees(result)
    else:
        print("Сотрудники не найдены.")


def save_to_csv(employees):
    """Сохранение сотрудников в CSV-файл."""
    try:
        with open(
            FILE_NAME, "w", newline="", encoding="utf-8-sig"
        ) as file:
            writer = csv.DictWriter(
                file, fieldnames=FIELDS, delimiter=";"
            )
            writer.writeheader()
            writer.writerows(employees)
        print("Данные сохранены в файл", FILE_NAME)
    except OSError as error:
        print("Ошибка сохранения файла:", error)


def load_from_csv():
    """Загрузка сотрудников из CSV-файла."""
    employees = []
    if not os.path.exists(FILE_NAME):
        print(
            "Файл пока не существует. Будет создан новый список."
        )
        return employees
    try:
        with open(
            FILE_NAME, "r", newline="", encoding="utf-8-sig"
        ) as file:
            reader = csv.DictReader(file, delimiter=";")
            if reader.fieldnames != FIELDS:
                raise ValueError("Неверная структура CSV файла.")
            for row in reader:
                age = int(row["Возраст"])
                salary = float(row["Оклад"])
                if age <= 0 or salary < 0:
                    raise ValueError(
                        "Некорректные данные сотрудника."
                    )
                employee = {
                    "Имя": row["Имя"],
                    "Фамилия": row["Фамилия"],
                    "Возраст": age,
                    "Должность": row["Должность"],
                    "Оклад": salary,
                    "Отдел": row["Отдел"],
                }
                employees.append(employee)
        print("Данные успешно загружены.")
    except (OSError, ValueError, csv.Error) as error:
        print("Ошибка загрузки данных:", error)
        return []
    return employees


def main():
    """Главная функция программы."""
    employees = load_from_csv()
    while True:
        print("\n===== БАЗА ДАННЫХ СОТРУДНИКОВ =====")
        print("1. Добавить сотрудника")
        print("2. Удалить сотрудника")
        print("3. Показать всех сотрудников")
        print("4. Сортировка")
        print("5. Фильтрация")
        print("6. Сохранить данные в CSV")
        print("7. Загрузить данные из CSV")
        print("0. Выход")
        choice = input("Выберите действие: ")
        if choice == "1":
            add_employee(employees)
        elif choice == "2":
            delete_employee(employees)
        elif choice == "3":
            show_employees(employees)
        elif choice == "4":
            sort_employees(employees)
        elif choice == "5":
            filter_employees(employees)
        elif choice == "6":
            save_to_csv(employees)
        elif choice == "7":
            employees = load_from_csv()
        elif choice == "0":
            save_to_csv(employees)
            print("Программа завершена.")
            break
        else:
            print("Неверный пункт меню. Попробуйте ещё раз.")


if __name__ == "__main__":
    main()