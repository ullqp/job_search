import pytest

from src.hh_api import HH_API
from src.reader_json import Reader_JSON
from src.vacancies import Vacancies


@pytest.fixture
def hh_api():
    hh_api = HH_API()
    return hh_api


@pytest.fixture
def reader_json():
    reader_json = Reader_JSON()
    return reader_json


@pytest.fixture
def vacancy():
    vacancy = Vacancies(
        "Python Developer",
        "<https://hh.ru/vacancy/123456>",
        "100 000-150 000 руб.",
        "Требования: опыт работы от 3 лет...",
    )
    return vacancy


@pytest.fixture
def vacancies_list():
    vacancies_list = [
        Vacancies("Vacancy 1", "", "50000 rub", "Требуется опыт работы в Python"),
        Vacancies("Vacancy 2", "", "150000 rub", "Работа с Java"),
        Vacancies("Vacancy 3", "", "75000 rub", "Обязанности: тестирование"),
    ]
    return vacancies_list
