import json
import os
from unittest.mock import MagicMock, mock_open, patch

from src.abc_reader_json import Reader_ABC
from src.vacancies import Vacancies


class Reader_JSON(Reader_ABC):
    """
    Реализация интерфейса для работы с вакансиями в JSON файле.

    Методы:
        read_vacancies(): Читает вакансии из файла и возвращает список объектов Vacancies.
        add_vacancy(vacancy): Добавляет новую вакансию в файл.
        delete_vacancies(vacancy): Удаляет указанную вакансию из файла.
    """

    def __init__(self, filename: str = "vacancies.json") -> None:
        """
        Инициализация объекта чтения/записи вакансий из JSON файла.

        Args:
            filename (str): Имя файла с данными. По умолчанию "vacancies.json".
        """

        self.__file_path = os.path.join("data", filename)

    @property
    def file_path(self) -> str:
        """
        Получение приватного поля пути файла.
        """

        return self.__file_path

    def read_vacancies(self) -> list[Vacancies]:
        """
        Читает вакансии из JSON файла и возвращает список объектов Vacancies.

        Возвращает:
            list: Список объектов Vacancies.
        """
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                if not isinstance(data, list):
                    data = [data] if data else []

                vacancies = []
                for item in data:
                    if isinstance(item, dict):
                        vacancy = Vacancies(
                            name=item.get("name", ""),
                            vacancies_url=item.get("url", ""),
                            salary=str(item.get("salary", 0)),
                            description=item.get("description", ""),
                        )
                        vacancy.currency = item.get("currency", "")
                        vacancies.append(vacancy)
                return vacancies

        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def add_vacancy(self, vacancy: Vacancies) -> bool:
        """
        Добавляет новую вакансию в файл.

        Args:
            vacancy (Vacancies): Объект вакансии для добавления.

        Возвращает:
            bool: True — успешно добавлено; False — если вакансия уже существует.
        """
        existing_vacancies = self.read_vacancies()

        for existing in existing_vacancies:
            if existing.vacancies_url == vacancy.vacancies_url:
                print(f"Вакансия уже существует: {vacancy.name}")
                return False

        existing_vacancies.append(vacancy)

        data_to_save = [
            {
                "name": v.name,
                "url": v.vacancies_url,
                "salary": v.salary,
                "currency": v.currency,
                "description": v.description,
            }
            for v in existing_vacancies
        ]

        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)

        return True

    def delete_vacancies(self, vacancy: Vacancies) -> bool:
        """
        Удаляет указанную вакансию из файла.

        Args:
            vacancy (Vacancies): Объект вакансии для удаления.

        Возвращает:
            bool: True — удалено; False — не найдено.
        """
        existing_vacancies = self.read_vacancies()

        updated_vacancies = [v for v in existing_vacancies if v.vacancies_url != vacancy.vacancies_url]

        if len(updated_vacancies) == len(existing_vacancies):
            print(f"Вакансия не найдена: {vacancy.name}")
            return False  # Вакансия не найдена

        data_to_save = [
            {
                "name": v.name,
                "url": v.vacancies_url,
                "salary": v.salary,
                "currency": v.currency,
                "description": v.description,
            }
            for v in updated_vacancies
        ]

        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)

        print(f"Вакансия удалена: {vacancy.name}")
        return True
