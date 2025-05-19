from src.hh_api import HH_API
from src.utils import filter_vacancies, get_top_vacancies, print_vacancies, sort_vacancies
from src.vacancies import Vacancies


def user_interaction() -> None:
    """
    Реализация интерфейса для пользователя.
    """

    hh_api = HH_API()

    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()

    hh_vacancies = hh_api.load_vacancies(search_query)

    vacancies_list = Vacancies.cast_to_object_list(hh_vacancies)

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)
