from src.hh_api import HH_API
from unittest.mock import patch, Mock


def test_init_HH_API(hh_api: HH_API) -> None:
    assert hh_api.url == "https://api.hh.ru/vacancies"
    assert hh_api.headers == {'User-Agent': 'HH-User-Agent'}
    assert hh_api.params == {'text': '', 'page': 0, 'per_page': 100}
    assert hh_api.vacancies == []


def test_HH_API_ABC__connect_true(hh_api: HH_API) -> None:
    assert hh_api._HH_API_ABC__connect()

def test_HH_API_ABC__connect_false(hh_api: HH_API) -> None:
    hh_api.url = "https://api.hh.ru/vacanciesfefe"
    assert not hh_api._HH_API_ABC__connect()


def test_load_vacancies_success(hh_api: HH_API) -> None:
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [{'id': 1, 'name': 'Vacancy 1 Python'}, {'id': 2, 'name': 'Python Vacancy 2'}]
        }
        mock_response.status_code = 200
        # Все вызовы возвращают один и тот же ответ
        mock_get.return_value = mock_response

        vacancies = hh_api.load_vacancies('Python')

        # Ожидаемое количество — количество итераций цикла (20) * элементов на страницу (2)
        assert len(vacancies) == 40

        # Проверка содержимого
        assert vacancies[0]['name'] == 'Vacancy 1 Python'


def test_load_vacancies_api_failure() -> None:
    api = HH_API()

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = api.load_vacancies('Python')

        assert result is None or result == []


