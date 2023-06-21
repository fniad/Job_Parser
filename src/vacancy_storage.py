from abc import ABC, abstractmethod
import json
from src.vacancy import Vacancy


class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, **kwargs):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        pass


class JSONVacancyStorage(VacancyStorage):
    def __init__(self, filename):
        self.filename = filename
        self.vacancies = []
        self.load_data()

    def __repr__(self):
        pass

    def __add__(self, other):
        """ Метод для сложения двух объектов JSONVacancyStorage """
        if not isinstance(other, JSONVacancyStorage):
            raise TypeError(f"операция сложения (+) не поддерживается для : "
                            f"'{type(self).__name__}' и '{type(other).__name__}'")
        filename = f"{self.filename.split('.')[0]}_{other.filename}"
        result = JSONVacancyStorage(filename)
        result.vacancies = self.vacancies + other.vacancies
        result.save_data()
        return result

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            pass

    def save_data(self):
        """Сохраняет полученный при помощи запроса результат в файл JSON"""
        data = [vars(vacancy) for vacancy in self.vacancies]
        with open('result_research_JSON/' + self.filename, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def add_vacancy(self, vacancy):
        if not isinstance(vacancy, Vacancy):
            raise TypeError(f'Вакансия {vacancy} должна быть экземпляром класса Vacancy.')
        self.vacancies.append(vacancy)
        self.save_data()

    def get_vacancies(self, **kwargs):
        return [vacancy for vacancy in self.vacancies if
                all(getattr(vacancy, key) == value for key, value in kwargs.items())]

    def delete_vacancy(self, vacancy_id):
        self.vacancies = [vacancy for vacancy in self.vacancies if vacancy.id != vacancy_id]
        self.save_data()
