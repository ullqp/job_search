# Создание экземпляра класса для работы с API сайтов с вакансиями
from src.reader_json import Reader_JSON
from src.user_utilities import user_interaction
from src.vacancies import Vacancies


if __name__ == "__main__":
    # Пример работы контструктора класса с одной вакансией
    vacancy = Vacancies(
        "Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.",
        "Требования: опыт работы от 3 лет..."
    )
    # Сохранение информации о вакансиях в файл
    json_saver = Reader_JSON()
    json_saver.add_vacancy(vacancy)
    vacancies = json_saver.read_vacancies()
    print(vacancies)
    json_saver.delete_vacancies(vacancy)

    user_interaction()
    json_saver = Reader_JSON()
    json_saver.add_vacancy(vacancy)
    json_saver.delete_vacancies(vacancy)