from src.utils import filter_vacancies, get_top_vacancies, print_vacancies, sort_vacancies
from src.vacancies import Vacancies


def test_sort_vacancies(vacancies_list: list[Vacancies]) -> None:

    sorted_list = sort_vacancies(vacancies_list)

    assert sorted_list[0].salary == 150000
    assert sorted_list[1].salary == 75000
    assert sorted_list[2].salary == 50000


def test_filter_vacancies(vacancies_list: list[Vacancies]) -> None:
    result = filter_vacancies(vacancies_list, ["Python"])
    assert len(result) == 1
    assert result[0].name == "Vacancy 1"

    result = filter_vacancies(vacancies_list, ["Java"])
    assert len(result) == 1
    assert result[0].name == "Vacancy 2"

    result = filter_vacancies(vacancies_list, ["C++"])
    assert len(result) == 0


def test_filter_vacancies_multiple(vacancies_list: list[Vacancies]) -> None:
    result = filter_vacancies(vacancies_list, ["Python", "тестирование"])
    names = [v.name for v in result]
    assert set(names) == {"Vacancy 1", "Vacancy 3"}


def test_get_top_vacancies(vacancies_list: list[Vacancies]) -> None:
    top2 = get_top_vacancies(vacancies_list, 2)
    assert top2 == vacancies_list[:2]
    assert len(top2) == 2


def test_print_vacancies(capsys, vacancies_list) -> None:
    print_vacancies(vacancies_list)
    captured = capsys.readouterr()
    assert str(vacancies_list) in captured.out
