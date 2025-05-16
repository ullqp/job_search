from abc import ABC, abstractmethod

from src.vacancies import Vacancies


class Reader_ABC(ABC):
    """
    Абстрактный базовый класс для чтения, добавления и удаления вакансий.

    Этот класс определяет интерфейс, который должны реализовать все конкретные
    классы-читатели вакансий, обеспечивающие работу с различными источниками данных.

    Методы:
        read_vacancies(): Получает список всех вакансий.
        add_vacancy(vacancy): Добавляет новую вакансию.
        delete_vacancies(vacancy): Удаляет указанную вакансию.
    """

    @abstractmethod
    def read_vacancies(self) -> list[Vacancies]:
        """
        Получает список всех вакансий.

        Возвращает:
            list: Список объектов или словарей, представляющих вакансии.
        """
        pass

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancies) -> bool:
        """
        Добавляет новую вакансию.

        Args:
            vacancy: Объект или структура данных, представляющая вакансию для добавления.
        """
        pass

    @abstractmethod
    def delete_vacancies(self, vacancy: Vacancies) -> bool:
        """
        Удаляет указанную вакансию.

        Args:
            vacancy: Объект или структура данных, указывающая на вакансию для удаления.

        Возвращает:
            bool: True, если удаление прошло успешно; False — если вакансия не найдена.
        """
        pass
