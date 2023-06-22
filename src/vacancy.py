class Vacancy:
    """Класс Вакансия"""
    def __init__(self, name, url, salary_from, salary_to, currency, description):
        """
        Инициализация экземпляра класса Вакансия
        """
        self.name = name
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.description = description

    def __repr__(self):
        return f"Вакансия (название = '{self.name}', зп = '{self.salary_from}' - {self.salary_to} {self.currency})"
