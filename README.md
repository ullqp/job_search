# Job Search: Парсер вакансий с hh.ru

Проект для поиска и анализа вакансий с платформы hh.ru через консольный интерфейс.

## Основные возможности

- Поиск вакансий по ключевым словам через API hh.ru
- Сохранение результатов в JSON-файл
- Фильтрация по описанию и зарплатному диапазону
- Топ-N вакансий по уровню зарплаты
- Управление сохраненными вакансиями (добавление/удаление)
- Покрытие тестами >80%

## Установка
Клонируйте репозиторий:
```bash
git clone https://github.com/ullqp/job_search.git
```

Использование
Пример работы с вакансиями
```python
from src.reader_json import Reader_JSON
from src.vacancies import Vacancies

# Создание и сохранение вакансии
vacancy = Vacancies(
    "Python Developer", 
    "https://hh.ru/vacancy/123456", 
    "100 000-150 000 руб.",
    "Требования: опыт работы от 3 лет..."
)

json_saver = Reader_JSON()
json_saver.add_vacancy(vacancy)  # Добавление в файл

# Чтение всех вакансий
all_vacancies = json_saver.read_vacancies()
print(f"Сохранено вакансий: {len(all_vacancies)}")

# Удаление вакансии
json_saver.delete_vacancies(vacancy)```
