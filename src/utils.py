
def filter_vacancies(vacancy_list):
    """
    Фильтрует вакансии из двух источников
    HeadHunter и SuperJob – по наименованию и возвращает отфильтрованный список вакансий."""
    return sorted(vacancy_list, key=lambda x: x.name)


def get_top_vacancies(vacancy_list, n):
    """Извлекает первые N вакансий из списка"""
    return vacancy_list[:n]


def sort_by_salary_from(vacancy_list):
    """
    Сортирует список вакансий по зарплате от большего к меньшему.
    """
    return sorted(vacancy_list, reverse=True)


def print_vacancies(vacancy_list):
    """Выводит информацию о вакансиях в консоль"""
    for vacancy in vacancy_list:
        if vacancy.currency not in ['RUR', 'RUB']:
            print(f"\n"
                  f"{vacancy.name.capitalize()}: {vacancy.salary_from} - {vacancy.salary_to} {vacancy.currency}\n"
                  f"В рублях максимальная заработная плата составит: {vacancy.currency_to_rub()} RUB\n"
                  f"{vacancy.url}\n"
                  f"------\n"
                  f"{vacancy.description}\n"
                  )
        else:
            if vacancy.currency == 'RUR':
                vacancy.currency = 'RUB'
            print(f"\n"
                  f"{vacancy.name.capitalize()}: {vacancy.salary_from} - {vacancy.salary_to} {vacancy.currency}\n"
                  f"{vacancy.url}\n"
                  f"------\n"
                  f"{vacancy.description}\n"
                  )


