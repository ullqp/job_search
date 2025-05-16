from src.vacancies import Vacancies

def sort_vacancies(vacancies_list: list[Vacancies]) -> list[Vacancies]:
    """
    Сортировка вакансий по уменьшению зарплаты.
    """

    return sorted(vacancies_list, key=lambda v: v.salary, reverse=True)


def filter_vacancies(vacancies_list: list[Vacancies], filter_words: list[str]) -> list[Vacancies]:
    """
    Фильтрация вакансий по указанному слову в описании.
    """
    if not filter_words:  # Если нет слов для фильтрации
        return vacancies_list.copy()

    filtered_vacancies = []
    filter_words_lower = [word.lower() for word in filter_words]

    for vacancy in vacancies_list:
        # Попытка получить requirement и responsibility
        requirement = getattr(vacancy, 'requirement', '') or ''
        responsibility = getattr(vacancy, 'responsibility', '') or ''

        # Если этих атрибутов нет, используем description
        if not requirement and not responsibility:
            description_text = getattr(vacancy, 'description', '') or ''
            full_text = description_text.lower()
        else:
            full_text = f"{requirement} {responsibility}".lower()

        # Проверяем совпадение хотя бы одного слова
        if any(word in full_text for word in filter_words_lower):
            filtered_vacancies.append(vacancy)

    return filtered_vacancies


def get_top_vacancies(vacancies_list: list[Vacancies], top_n: int) -> list[Vacancies]:
    """
    Получение топа-N вакансий.
    """
    return vacancies_list[:top_n]


def print_vacancies(vacancies_list: list[Vacancies]) -> None:
    """
    Вывод вакансий в консоль
    """
    print(vacancies_list)