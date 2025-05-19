from typing import Any


class Vacancies:
    """
    Класс для представления вакансии с информацией о названии, URL, зарплате, валюте и описании.

    Атрибуты:
        name (str): Название вакансии.
        vacancies_url (str): Ссылка на вакансию.
        salary (float): Средняя зарплата (числовое значение).
        currency (str): Валюта зарплаты.
        description (str): Описание вакансии.
    """

    __slots__ = ["name", "vacancies_url", "salary", "currency", "description"]

    def __init__(self, name: str, vacancies_url: str, salary: str, description: str) -> None:
        """
        Инициализация объекта вакансии.

        Args:
            name (str): Название вакансии.
            vacancies_url (str): URL вакансии.
            salary (str): Строка с описанием зарплаты, например "100000-150000 руб".
            description (str): Описание вакансии.
        """
        self.name = name
        self.vacancies_url = vacancies_url
        self.salary = self.__validate_salary(salary)[0]
        self.currency = self.__validate_salary(salary)[1]
        self.description = description

    def __str__(self) -> str:
        return (
            f"Vacancies(name={self.name!r}, url={self.vacancies_url!r}, "
            f"salary={self.salary!r}, description={self.description!r})"
        )

    def __repr__(self) -> str:
        return (
            f"Vacancies(name={self.name!r}, url={self.vacancies_url!r}, "
            f"salary={self.salary!r}, description={self.description!r})"
        )

    def __lt__(self, other) -> bool:
        """Проверка, что текущая зарплата меньше другой."""
        if not isinstance(other, Vacancies):
            return NotImplemented
        return self.salary < other.salary

    def __gt__(self, other) -> bool:
        """Проверка, что текущая зарплата больше другой."""
        if not isinstance(other, Vacancies):
            return NotImplemented
        return self.salary > other.salary

    def __validate_salary(self, salary: str) -> tuple[float, str]:
        """
        Внутренний метод для обработки строки зарплаты и получения числового значения и валюты.

        Args:
            salary (str): Строка с зарплатой, например "100000-150000 руб" или "150000 руб".

        Returns:
            tuple: (salary_value (float), currency (str))
                - salary_value: Средняя зарплата или 0 при ошибке.
                - currency: Валюта зарплаты или пустая строка при ошибке.
        """
        if not salary:
            return 0.0, ""

        salary = salary.strip()
        currency = ""

        try:
            if "-" in salary:
                # Обработка диапазона зарплат "100000-150000 руб"
                parts = salary.split("-")
                min_part = parts[0].strip()
                max_part = parts[1].strip()

                # Извлекаем числовые значения
                min_salary = int(min_part.replace(" ", ""))
                max_salary_parts = max_part.split()
                max_salary = int("".join(max_salary_parts[:-1]))
                currency = max_salary_parts[-1]

                # Вычисляем среднее значение
                salary_value = (min_salary + max_salary) / 2
                return float(salary_value), currency

            elif any(char.isdigit() for char in salary):
                # Обработка фиксированной зарплаты "150000 руб"
                parts = salary.split()
                salary_value = int("".join(parts[:-1]))
                currency = parts[-1]
                return float(salary_value), currency

        except (ValueError, IndexError, AttributeError):
            pass

        # Возвращаем значения по умолчанию в случае ошибки
        return 0.0, ""

    @classmethod
    def cast_to_object_list(cls, hh_vacancies: Any) -> list:
        """
        Преобразует JSON из HH в список объектов Vacancies.
        """
        result = []

        for item in hh_vacancies:
            # Основные поля
            name = item.get("name", "")
            url = item.get("alternate_url", "")
            description = ""

            # Обработка snippet для description
            snippet = item.get("snippet")
            if snippet and isinstance(snippet, dict):
                description = snippet.get("requirement", "")

            # Обработка зарплаты
            salary_data = item.get("salary")
            if salary_data:
                from_salary = salary_data.get("from")
                to_salary = salary_data.get("to")
                currency = salary_data.get("currency", "RUB")
                if from_salary is not None and to_salary is not None:
                    salary_str = f"{from_salary}-{to_salary} {currency}"
                elif from_salary is not None:
                    salary_str = f"от {from_salary} {currency}"
                elif to_salary is not None:
                    salary_str = f"до {to_salary} {currency}"
                else:
                    salary_str = "0"
            else:
                salary_str = "0"

            # Создаем объект вакансии
            vacancy = cls(name=name, vacancies_url=url, salary=salary_str, description=description)
            result.append(vacancy)

        return result
