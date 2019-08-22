"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from customer import Customer
import statistics
import datetime


class CustomerList:
    """Класс CustomerList представляет список клиентов.

    Атрибуты экземпляра класса:
        - self.customers (list из Customer): список клиентов;
        - self.filename (str): имя файла, из которого были получены клиенты;
        - self.errors (list из str): список строк с ошибками чтения файла.
    """

    def __init__(self):
        self.customers = []
        self.filename = ""
        self.errors = []

    def __str__(self):
        line = "Список клиентов ({len_data}):\n".format(
                len_data=len(self.customers))
        pattern_line = "{index}. {customer}\n"
        for index, customer in enumerate(self.customers):
            line += pattern_line.format(
                index=index + 1,
                customer=str(customer))

        return line[:-1]

    def open(self, filename):
        self.customers = []
        self.errors = []
        self.filename = filename

        with open(filename, "r", encoding="UTF-8") as fh:
            for line in fh:
                try:
                    customer = Customer.from_string(line)
                    self.customers.append(customer)
                except Exception as err:
                    self.errors.append(str(err))

        assert len(self.customers) > 0, "Нет данных для обработки!"

        self.customers = sorted(
            self.customers,
            key=lambda customer: customer.f + customer.i + customer.o)

    def total_price(self):
        return sum(customer.polis_price for customer in self.customers)

    def price_stats(self):
        list_of_polis_price = list(
            (customer.polis_price for customer in self.customers))

        mean = statistics.mean(list_of_polis_price)
        median = statistics.median(list_of_polis_price)
        try:
            mode = statistics.mode(list_of_polis_price)
        except Exception:
            mode = "не доступно"

        return mean, mode, median

    def age_stats(self):
        list_of_customers_years = []
        for customer in self.customers:
            year = int(datetime.date.today().year - customer.birthday.year)
            list_of_customers_years.append(year)

        mean = statistics.mean(list_of_customers_years)
        median = statistics.median(list_of_customers_years)

        return int(mean), int(median)

    def most_popular_polis_type(self):
        dict_polis = {}
        for customer in self.customers:
            if customer.polis_type in dict_polis.keys():
                dict_polis[customer.polis_type] += 1
            else:
                dict_polis[customer.polis_type] = 1

        list_of_polis = list(sorted(
            dict_polis,
            key=lambda polis: dict_polis[polis], reverse=True))

        return (list_of_polis[0], dict_polis[list_of_polis[0]])

    def most_profitable_polis_type(self):
        dict_polis = {}
        for customer in self.customers:
            if customer.polis_type in dict_polis.keys():
                dict_polis[customer.polis_type] += customer.polis_price
            else:
                dict_polis[customer.polis_type] = customer.polis_price

        list_of_polis = list(sorted(
            dict_polis,
            key=lambda polis: dict_polis[polis], reverse=True))

        return (list_of_polis[0], dict_polis[list_of_polis[0]])

    def print_report(self):
        sum_price = self.total_price()
        mean_price, moda_price, median_price = self.price_stats()
        mean_age, median_age = self.age_stats()
        name_popular_polis, count_popular_polis = \
            self.most_popular_polis_type()
        name_profitable_polis, sum_profitable_polis = \
            self.most_profitable_polis_type()

        report = "Сумма контрактов = {sum_price:,} руб.\n\n" \
            "Статистика продаж:\n" \
            "  - Цена: " \
            "{mean_price:,} руб. (среднее), " \
            "{moda_price:,} руб. (мода), " \
            "{median_price:,.1f} руб. (медиана)\n" \
            "  - Возраст: " \
            "{mean_age:.1f} л. (среднее), " \
            "{median_age:.1f} л. (медиана)\n" \
            "  - Самый популярный тип страхового полиса: " \
            "{name_popular_polis} ({count_popular_polis})\n" \
            "  - Самый прибыльный тип страхового полиса: " \
            "{name_profitable_polis} ({sum_profitable_polis:,} руб.)".format(
                sum_price=sum_price,
                mean_price=mean_price,
                moda_price=moda_price,
                median_price=median_price,
                mean_age=mean_age,
                median_age=median_age,
                name_popular_polis=name_popular_polis,
                count_popular_polis=count_popular_polis,
                name_profitable_polis=name_profitable_polis,
                sum_profitable_polis=sum_profitable_polis)

        print(report)
