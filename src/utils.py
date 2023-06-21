def filter_vacancies(vacancies, filter_words):
    """
    Фильтрует вакансии из двух источников
    HeadHunter и SuperJob – по наименованию и возвращает отфильтрованный список вакансий."""
    filtered_vacancies = []
    if vacancies is not None:
        vacancies = vacancies.get_vacancies()
        for vacancy in vacancies:
            if all(word.lower() in vacancy.name or
                   word.lower() in vacancy.description for word in filter_words):
                filtered_vacancies.append(vacancy)
    return filtered_vacancies


def sort_vacancies(vacancies):
    """Сортирует список вакансий по максимальной зарплате в убывающем порядке"""
    sorted_vacancies = sorted(
        [vacancy for vacancy in vacancies if vacancy.salary_to and vacancy.salary_to != "По договорённости"],
        key=lambda x: x.salary_to,
        reverse=True)
    return sorted_vacancies


def get_top_vacancies(vacancies, n):
    """Извлекает первые N вакансий из списка"""
    return vacancies[:n]


def print_vacancies(vacancies):
    """Выводит информацию о вакансиях в консоль"""
    for vacancy in vacancies:
        if vacancy.description != '':
            print(f"\n"
                  f"{vacancy.name.capitalize()}: {vacancy.salary_from} - {vacancy.salary_to} {vacancy.currency}\n"
                  f"{vacancy.url}\n"
                  f"---\n"
                  f"{vacancy.description}\n\n"
                  f"------")
        else:
            print(f"\n"
                  f"{vacancy.name.capitalize()}: {vacancy.salary_from} - {vacancy.salary_to} {vacancy.currency}\n\n"
                  f"------")

