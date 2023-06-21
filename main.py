from src.utils import sort_vacancies, get_top_vacancies, print_vacancies, \
    filter_vacancies
from src.vacancy_api import SuperJobAPI, HeadHunterAPI

# # json_saver.get_vacancies_by_salary("100 000-150 000 руб.")
# json_saver.delete_vacancy(vacancy)


# Функция для взаимодействия с пользователем
def main():
    platforms = ["HeadHunter", "SuperJob"]
    platform = None
    sj_vacancies = None
    hh_vacancies = None
    filtered_vacancies = None

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

        # Получение вакансий с разных платформ
        if platform == "HeadHunter":
            hh_vacancies = HeadHunterAPI(keyword).get_vacancies()
            filtered_vacancies = filter_vacancies(hh_vacancies, keyword)
        elif platform == "SuperJob":
            sj_vacancies = SuperJobAPI(keyword).get_vacancies()
            filtered_vacancies = filter_vacancies(sj_vacancies, keyword)
        elif platform == platforms:
            vacancies_json = sj_vacancies + hh_vacancies    # не складывается Х(
            filtered_vacancies = filter_vacancies(vacancies_json, keyword)

        print(f'Найдено {len(filtered_vacancies)} вакансий.')
        top_n = int(input("Введите количество вакансий для вывода в топ N, числом: "))

        if not filtered_vacancies:
            print("Нет вакансий, соответствующих заданным критериям.")
            return

        sorted_vacancies = sort_vacancies(filtered_vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
        print_vacancies(top_vacancies)


main()
