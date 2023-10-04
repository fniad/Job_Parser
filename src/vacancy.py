from src.cbr_currency import currency_data


class Vacancy:
    """Класс Вакансия"""
    currency_data = currency_data

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

    def __eq__(self, other):
        return self.currency_to_rub() == other.currency_to_rub()

    def __lt__(self, other):
        return self.currency_to_rub() < other.currency_to_rub()

    def __gt__(self, other):
        return self.currency_to_rub() > other.currency_to_rub()

    def currency_to_rub(self):
        """Конвертация в рубли"""
        if self.currency in self.currency_data:
            conv_rate = float(self.currency_data[self.currency])
        else:
            conv_rate = 1.0  # Дефолтное значение

        return round((self.salary_to * conv_rate), 1)
