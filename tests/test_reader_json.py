import json
from unittest.mock import mock_open, patch

from src.reader_json import Reader_JSON
from src.vacancies import Vacancies


def test_init_reader_json(reader_json: Reader_JSON):
    assert reader_json.file_path == 'data\\vacancies.json'

def test_read_vacancies_success() -> None:
    # Мокаем содержимое файла — список вакансий
    mock_data = [
        {
            "name": "Python Developer",
            "url": "https://example.com/vacancy1",
            "salary": "100000 р"
,
            "description": "Работа с Python",
            "currency": "USD"
        },
        {
            "name": "Data Scientist",
            "url": "https://example.com/vacancy2",
            "salary": "120000 р"
,
            "description": "Аналитика данных",
            "currency": "USD"
        }
    ]
    mock_json = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_json)):
        reader = Reader_JSON("vacancies.json")
        vacancies = reader.read_vacancies()

        assert len(vacancies) == 2
        assert vacancies[0].name == "Python Developer"
        assert vacancies[0].vacancies_url == "https://example.com/vacancy1"
        assert vacancies[0].salary == 100000


def test_add_vacancy_already_exists() -> None:
    # Создаем объект менеджера
    manager = Reader_JSON("fake_path.json")

    # Мокаем read_vacancies так, чтобы он возвращал список с вакансиями
    existing_vacancy = Vacancies(
        name="Existing Vacancy",
        vacancies_url="https://example.com/vacancy1",
        salary="100000",
        description="Описание",
    )

    with patch.object(manager, 'read_vacancies', return_value=[existing_vacancy]):
        # Создаем новую вакансию с тем же URL
        new_vacancy = Vacancies(
            name="New Vacancy",
            vacancies_url="https://example.com/vacancy1",  # тот же URL
            salary="120000",
            description="Новое описание",
        )

        result = manager.add_vacancy(new_vacancy)
        assert result is False  # Уже существует


def test_add_new_vacancy_success() -> None:
    manager = Reader_JSON("fake_path.json")

    with patch.object(manager, 'read_vacancies', return_value=[]):
        new_vacancy = Vacancies(
            name="New Vacancy",
            vacancies_url="https://example.com/vacancy2",
            salary="120000",
            description="Новое описание",
        )

        m_open = mock_open()
        with patch("builtins.open", m_open):
            result = manager.add_vacancy(new_vacancy)
            assert result is True

            m_open.assert_any_call("data\\fake_path.json", "w", encoding="utf-8")


def test_delete_vacancy() -> None:
    manager = Reader_JSON("fake_path.json")
    existing_vacancies = [
        Vacancies("Вакансия 1", "https://example.com/vacancy1", "100000", "Описание 1"),
        Vacancies("Вакансия 2", "https://example.com/vacancy2", "120000", "Описание 2"),
    ]
    with patch.object(manager, 'read_vacancies', return_value=existing_vacancies):
        vacancy_to_delete = Vacancies("Вакансия 2", "https://example.com/vacancy2", "120000", "Описание 2")
        written_contents = []

        with patch("builtins.open", mock_open()) as m_open:
            # Настраиваем так, чтобы write() сохранял данные
            m_open.return_value.__enter__.return_value.write.side_effect = lambda data: written_contents.append(data)
            result = manager.delete_vacancies(vacancy_to_delete)

            assert result is True
            import os
            m_open.assert_called_once_with(os.path.join('data', 'fake_path.json'), 'w', encoding='utf-8')

            # Объединяем все записанные строки и парсим как JSON
            json_str = ''.join(written_contents)
            import json
            data_loaded = json.loads(json_str)

            # Проверка отсутствия удаленной вакансии
            assert all(v["url"] != "https://example.com/vacancy2" for v in data_loaded)
