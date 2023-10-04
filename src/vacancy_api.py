from abc import ABC, abstractmethod
from configparser import ParsingError
import requests
import os
from dotenv import load_dotenv

load_dotenv('.env')


class VacancyAPI(ABC):

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def get_formatted_vacancies(self):
        pass


class HeadHunterAPI(VacancyAPI):
    url = 'https://api.hh.ru/vacancies'

    def __init__(self, keyword):
        self.headers = {'User-Agent': 'job_parser/1.0 (artkamproject@gmail.com)'}
        self.params = {
            'per_page': 100,
            'page': None,
            'text': keyword,
            'archive': False,
            'only_with_salary': True
        }
        self.keyword = keyword
        self.vacancies = []

    def get_request(self):
        """Запрашивает с HH запрос на получение вакансий"""
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            return response.json()['items']
        else:
            raise ParsingError(f'Ошибка получения вакансий! Статус: {response.status_code}')

    def get_vacancies(self, page_count=2):
        """Парсит вакансии с указанного пользователем количества страниц"""
        self.vacancies = []  # очищает список
        for page in range(page_count):
            page_vacancies = []
            self.params['page'] = page
            print(f'{self.__class__.__name__} парсинг страницы {page+1} HH -', end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f'Загружено вакансий: {len(page_vacancies)}')
            if len(page_vacancies) == 0:
                print(f"Не удалось загрузить страницу {page + 1}")
                break

    def get_formatted_vacancies(self):
        """
        Приводит полученные вакансии к единому виду.
        Возвращает список со словарями по каждой из вакансий.
        """
        formatted_vacancies = []

        for vacancy in self.vacancies:
            formatted_vacancy = {
                'name': vacancy['name'].lower(),
                'url': vacancy['alternate_url'],
                'salary_from': vacancy['salary']['from'] if vacancy['salary']['from'] is not None else 0,
                'salary_to': vacancy['salary']['to'] if vacancy['salary']['to'] is not None else vacancy['salary']['from'],
                'currency': vacancy['salary']['currency'] if vacancy['salary'] else '',
                'description': vacancy['snippet']['requirement'] if vacancy['snippet']['requirement'] is not None else ''
            }
            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies


class SuperJobAPI(VacancyAPI):
    url = 'https://api.superjob.ru/2.0/vacancies/'

    def __init__(self, keyword):
        self.params = {
            'count': 100,
            'page': None,
            'keyword': keyword,
            'archive': False,
            'agreement': False
        }
        self.secret_key: str = os.getenv('SECRET_KEY_SJ')
        self.headers = {'X-Api-App-Id': self.secret_key}
        self.keyword = keyword
        self.vacancies = []

    def get_request(self):
        """Запрашивает с SJ запрос на получение вакансий"""
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            return response.json()['objects']
        else:
            raise ParsingError(f'Ошибка получения вакансий! Статус: {response.status_code}')

    def get_vacancies(self, page_count=2):
        """Парсит вакансии с указанного пользователем количества страниц"""
        self.vacancies = []  # очищает список
        for page in range(page_count):
            page_vacancies = []
            self.params['page'] = page
            print(f'{self.__class__.__name__} парсинг страницы {page+1} SJ -', end=" ")
            try:
                page_vacancies = self.get_request()
                if len(page_vacancies) == 0:
                    print(f'На странице {page + 1} нет вакансий, удовлетворяющих запросу')
                    break
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f'Загружено вакансий: {len(page_vacancies)}')

    def get_formatted_vacancies(self):
        """
        Приводит полученные вакансии к единому виду.
        Возвращает список со словарями по каждой из вакансий.
        """
        formatted_vacancies = []

        for vacancy in self.vacancies:
            formatted_vacancy = {
                'name': vacancy['profession'].lower(),
                'url': vacancy['link'],
                'salary_from': vacancy['payment_from'] if vacancy['payment_from'] is not None else 0,
                'salary_to': vacancy['payment_to'] if vacancy['payment_to'] != 0 else vacancy['payment_from'],
                'currency': vacancy["currency"].upper(),
                'description': vacancy['candidat'].lower()
            }
            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies
