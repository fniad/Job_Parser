from abc import ABC, abstractmethod
import json
from src.vacancy import Vacancy
from src.cbr_currency import currency_data


class VacancyStorage(ABC):

    @abstractmethod
    def save_data(self, json_file):
        pass

    @abstractmethod
    def add_vacancy(self):
        pass


class JSONVacancyStorage(VacancyStorage):
    currency_data = currency_data

    def __init__(self, keyword, vacancies_json):
        self.keyword = keyword
        self.filename = 'result_research_JSON/' + f'{self.keyword}.json'
        self.save_data(vacancies_json)
        self.vacancy_list = []

    def save_data(self, vacancies_json):
        """Сохраняет полученный при помощи запроса результат в файл JSON"""
        with open(self.filename, 'w') as file:
            json.dump(vacancies_json, file, indent=4, ensure_ascii=False)

    def add_vacancy(self):
        """Добавляет вакансии как экземпляры класса Вакансия"""
        with open(self.filename, 'r', encoding='utf-8') as file:
            vacancies = json.load(file)

        for vacancy in vacancies:
            new_vacancy = Vacancy(vacancy["name"], vacancy["url"], vacancy["salary_from"], vacancy["salary_to"],
                                  vacancy["currency"], vacancy["description"])
            self.vacancy_list.append(new_vacancy)
        return self.vacancy_list

    def filter_vacancies(self):
        """
        Фильтрует вакансии из двух источников
        HeadHunter и SuperJob – по наименованию и возвращает отфильтрованный список вакансий."""
        self.vacancy_list = sorted(self.vacancy_list, key=lambda x: x.name)
        return self.vacancy_list

    def get_top_vacancies(self, n):
        """Извлекает первые N вакансий из списка"""
        self.vacancy_list = self.vacancy_list[:n]

    def sort_by_salary_from(self):
        """
        Сортирует список вакансий по зарплате от большего к меньшему.
        :param vacancies: список объектов Vacancy
        :param currency_data: словарь с данными о курсах валют
        :return: отсортированный список объектов Vacancy
        """
        rub_course = self.currency_data.get('RUB', 1)  # получаем курс рубля из словаря
        self.vacancy_list = sorted(self.vacancy_list,
                                   key=lambda x: (isinstance(x.salary_to, int),
                                                  x.salary_to * self.currency_data.get(x.currency, 1) * rub_course,
                                                  x.currency), reverse=True)

    def print_vacancies(self):
        """Выводит информацию о вакансиях в консоль"""
        for vacancy in self.vacancy_list:
            if vacancy.currency not in ['RUR', 'RUB']:
                print(f"\n"
                      f"{vacancy.name.capitalize()}: {vacancy.salary_from} - {vacancy.salary_to} {vacancy.currency}\n"
                      f"В рублях максимальная заработная плата составит: {self.currency_to_rub(vacancy)} RUB\n"
                      f"{vacancy.url}\n"
                      f"------\n"
                      f"{vacancy.description}\n"
                      )
            else:
                if vacancy.currency == 'RUR':
                    vacancy.currency = 'RUB'
                print(f"\n"
                      f"{vacancy.name.capitalize()}: {vacancy.salary_from} - {vacancy.salary_to} {vacancy.currency}\n"
                      f"------\n"
                      f"{vacancy.description}\n"
                      )

    @classmethod
    def currency_to_rub(cls, vacancy):
        """Конвертация в рубли"""
        if vacancy.currency in cls.currency_data:
            conv_rate = float(cls.currency_data[vacancy.currency])
        else:
            conv_rate = 1.0  # Дефолтное значение

        return round((vacancy.salary_to * conv_rate), 1)
