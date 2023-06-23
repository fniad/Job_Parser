from src.vacancy_api import SuperJobAPI, HeadHunterAPI
from src.vacancy_storage import JSONVacancyStorage
from src.utils import filter_vacancies, sort_by_salary_from, get_top_vacancies, print_vacancies
from os import getenv
from dotenv import load_dotenv


# Функция для взаимодействия с пользователем
def main():
    platforms = ["HeadHunter", "SuperJob"]
    platform = None
    vacancies_in_json = []

    # Выбор пользователем платформы
    try:
        selected_platform = int(input("Выберите платформу, где будут искаться вакансии:\n"
                                      "1 - HeadHunter,\n"
                                      "2 - SuperJob,\n"
                                      "3 - обе платформы\n"
                                      "4 - я передумал, хочу выйти\n\n"))
    except ValueError:
        print("Значение должно быть числом от 1 до 4.")
    else:
        while selected_platform not in [1, 2, 3, 4]:
            try:
                selected_platform = int(input("Неверно выбрана платформа. Введите число из предложенных.\n"))
            except ValueError:
                print("Значение должно быть числом от 1 до 4.")
        if selected_platform == 1:
            platform = platforms[0]
        elif selected_platform == 2:
            platform = platforms[1]
        elif selected_platform == 3:
            platform = platforms
        elif selected_platform == 4:
            exit()

        # Вывод пользователю сообщения о выбранных платформах
        if platform != platforms:
            print(f'Вы выбрали платформу {platform}')
        else:
            print(f"Вы выбрали обе платформы: HeadHunter и SuperJob")

        # Получение от пользователя запроса
        keyword = input("Введите ключевое слово для поиска.\n"
                        "Например, 'Python'\n").lower()
        try:
            page_count = int(input("Введите количество страниц, с которых хотите получить результат: "))
        except ValueError:
            print("начение должно быть числом.")
            page_count = int(input("Введите количество страниц, с которых хотите получить результат: "))

        # Получение вакансий с разных платформ
        hh = HeadHunterAPI(keyword)
        sj = SuperJobAPI(keyword)
        if platform == "HeadHunter":
            hh.get_vacancies(page_count)
            vacancies_in_json.extend(hh.get_formatted_vacancies())
        elif platform == "SuperJob":
            sj.get_vacancies(page_count)
            vacancies_in_json.extend(sj.get_formatted_vacancies())
        elif platform == platforms:
            for api in (hh, sj):
                api.get_vacancies(page_count)
                vacancies_in_json.extend(api.get_formatted_vacancies())

        vacancies = JSONVacancyStorage(keyword, vacancies_in_json)
        filter_vac = filter_vacancies(vacancies.add_vacancy())
        print(f'\nВсего вакансий выгружено:{len(filter_vac)}')
        top_n = int(input("Введите количество вакансий для вывода в топ N по зарплате, числом: "))

        if not filter_vac:
            print("Нет вакансий, соответствующих заданным критериям.")
            return

        sorted_vac = sort_by_salary_from(filter_vac)
        top_vac = get_top_vacancies(sorted_vac, top_n)
        print_vacancies(top_vac)


main()
