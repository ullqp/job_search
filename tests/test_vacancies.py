from src.vacancies import Vacancies
from tests.conftest import vacancy


def test_vacancy_init(vacancy: Vacancies) -> None:
    assert vacancy.name == "Python Developer"
    assert vacancy.vacancies_url == "<https://hh.ru/vacancy/123456>"
    assert vacancy.description == "Требования: опыт работы от 3 лет..."


def test_validate_salary_1() -> None:
    vacancy = Vacancies("abc", "abc_url", "100 000 000 rub", "cba")
    assert vacancy.salary == 100000000


def test_not_validate_salary() -> None:
    vacancy = Vacancies("abc", "abc_url", "100345", "cba")
    assert vacancy.salary == 0.0


def test_cast_to_object_list() -> None:
    json_data = [
        {
            "name": "Разработчик",
            "alternate_url": "https://example.com/vacancy/1",
            "snippet": {"requirement": "Опыт работы от 3 лет"},
            "salary": {
                "from": 100000,
                "to": 150000,
                "currency": "RUB"
            }
        },
        {
            "name": "Дизайнер",
            "alternate_url": "https://example.com/vacancy/2",
            # Без snippet
            "salary": {
                "from": 80000,
                "to": 120000,
                "currency": "RUB"
            }
        },
        {
            "name": "Менеджер",
            "alternate_url": "https://example.com/vacancy/3",
            # Без salary
        }
    ]

    vacancies = Vacancies.cast_to_object_list(json_data)

    assert len(vacancies) == 3

    v1 = vacancies[0]
    assert v1.name == "Разработчик"
    assert v1.vacancies_url == "https://example.com/vacancy/1"
    assert v1.description == "Опыт работы от 3 лет"
    assert abs(v1.salary - ((100000 + 150000) / 2)) < 1e-6
    assert v1.currency == "RUB"

    v2 = vacancies[1]
    assert v2.description == ""
    assert abs(v2.salary - ((80000 + 120000) / 2)) < 1e-6
    assert v2.currency == "RUB"

    v3 = vacancies[2]
    assert v3.description == ""
    assert v3.salary == 0.0
    assert v3.currency == ""
