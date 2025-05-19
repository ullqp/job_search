import requests

from src.abc_hh_api import HH_API_ABC
from src.vacancies import Vacancies


class HH_API(HH_API_ABC):
    """
    Реализации API-оберток по поиску вакансий.

    Этот класс задает интерфейс, который должны реализовать все конкретные классы,
    взаимодействующие с API различных сервисов по поиску вакансий.

    Методы:
      __connect(): Устанавливает соединение с API сервиса.
      load_vacancies(keyword): Загружает список вакансий по заданному ключевому слову.
    """

    def __init__(self) -> None:
        """
        Инициализация объекта API-обертки.
        """
        self.__url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": 100}
        self.vacancies = []

    def _HH_API_ABC__connect(self) -> bool:
        """
        Проверка доступности API
        """
        return True if requests.get(self.__url).status_code == 200 else False

    def load_vacancies(self, keyword) -> list[Vacancies] | None:
        """
        Загрузка список вакансий по заданному ключевому слову.
        """
        if self._HH_API_ABC__connect():
            self.params["text"] = keyword
            while self.params.get("page") != 20:
                response = requests.get(self.__url, headers=self.headers, params=self.params)
                vacancies = response.json()["items"]
                self.vacancies.extend(vacancies)
                self.params["page"] += 1
            return self.vacancies
        else:
            print("ошибка")
