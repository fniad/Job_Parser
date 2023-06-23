from abc import ABC, abstractmethod
import json
from src.vacancy import Vacancy


class VacancyStorage(ABC):

    @abstractmethod
    def save_data(self, json_file):
        pass

    @abstractmethod
    def add_vacancy(self):
        pass

    @abstractmethod
    def del_vacancy(self):
        pass


class JSONVacancyStorage(VacancyStorage):

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

    def del_vacancy(self):
        """Очистит от вакансий файл JSON"""
        with open(self.filename, 'w') as file:
            json.dump('', file, indent=4, ensure_ascii=False)
