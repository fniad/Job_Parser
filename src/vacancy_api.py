from abc import ABC, abstractmethod
import requests
from src.vacancy import Vacancy
from src.vacancy_storage import JSONVacancyStorage


class VacancyAPI(ABC):

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(VacancyAPI):
    url = 'https://api.hh.ru/vacancies'

    def __init__(self, keyword):
        self.headers = {'User-Agent': 'job_parser/1.0 (artkamproject@gmail.com)'}
        self.params = {
            'count': 100,
            'page': 2,
            'text': keyword,
            'archive': False,
        }
        self.keyword = keyword

    def get_request(self):

        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f'Error {response.status_code}: {response.text}')

    def get_vacancies(self):
        """Добавляет вакансии с HH в JSON-файл"""
        hh_vacancies = self.get_request()
        hh_json_saver = JSONVacancyStorage(filename=f'{self.keyword}_hh.json')
        for vacancy in hh_vacancies['items']:
            hh_json_saver.add_vacancy(Vacancy(
                name=vacancy['name'].lower(),
                url=vacancy['alternate_url'],
                salary_from=vacancy['salary'].get('from') if vacancy['salary'] else 'По договорённости',
                salary_to=vacancy['salary'].get('to') if vacancy['salary'] else '',
                currency=vacancy['salary'].get("currency") if vacancy['salary'] else '',
                description=vacancy['snippet']['requirement']
            ))
        return hh_json_saver


class SuperJobAPI(VacancyAPI):
    url = 'https://api.superjob.ru/2.0/vacancies/'

    def __init__(self, keyword):
        self.params = {
            'keyword': keyword,
            'archive': False,
        }
        self.secret_key = \
            'v3.r.122993083.0a5f72aa9f17292590a9f67f83232425af144c3a.7f4c5ad671b9f5286c5c2cbf3c771ed31d6c817e'
        self.headers = {'X-Api-App-Id': self.secret_key}
        self.keyword = keyword

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f'Error {response.status_code}: {response.text}')

    def get_vacancies(self):
        """Добавляет вакансии с SJ в JSON-файл"""
        superjob_vacancies = self.get_request()
        sj_json_saver = JSONVacancyStorage(filename=f'{self.keyword}_sj.json')
        for vacancy in superjob_vacancies['objects']:
            sj_json_saver.add_vacancy(Vacancy(
                name=vacancy['profession'].lower(),
                url=vacancy['link'],
                salary_from=vacancy['payment_from'],
                salary_to=vacancy['payment_to'],
                currency=vacancy["currency"],
                description=vacancy['candidat'].lower(),
            ))
        return sj_json_saver
