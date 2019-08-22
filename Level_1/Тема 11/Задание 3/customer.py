"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import re
import datetime


class Customer:
    """Класс Customer представляет клиента.

    Атрибуты экземпляра класса:
      - self.info: словарь-информация о клиенте; содержит следующие ключи:
        - f (str): фамилия клиента;
        - i (str): имя клиента;
        - o (str): отчество клиента;
        - birthday (datetime.date): дата рождения;
        - polis_type (str): тип полиса;
        - polis_price (int): цена оформленного полиса.
    """
    def __init__(self, info):
        """Инициализация класса.

        Аргументы:
          - info (dict): словарь-информация о клиенте (формата 'self.info')

        Необходимые проверки:
          - info - словарь и содержит необходимые ключи;
          - значения в словаре имеют нужный тип.

        Исключения:
          - ValueError - если не все проверки успешны.

        Действия:
          - установить self.info;
          - Ф, И, О и тип полиса должны быть с большой буквы.
        """
        key_tuple = ("f", "i", "o", "birthday", "polis_type", "polis_price")

        # Список ошибок
        error_line = list()
        error_line.append(
            "Словарь не содержит необходимые ключи \"{key}\"!")
        error_line.append("Словарь содержит сторонние ключи \"{key}\"!")
        error_line.append("Некорретный тип значения в ключе \"{key}\"!")
        error_line.append(
            "Значине не начинается с большой буквы! \"{value}\"!")
        if not isinstance(info, dict):
            raise ValueError("Переданный аргумент не словарь!")

        for key in key_tuple:
            try:
                info[key]
            except Exception:
                raise ValueError(error_line[0].format(key=key))

        for key, value in info.items():
            if not(key in key_tuple):
                raise ValueError(error_line[1].format(key=key))

            if key != key_tuple[3] and key != key_tuple[5]:
                if not isinstance(value, str):
                    raise ValueError(
                        error_line[2].format(key=key))
                info[key] = value.capitalize()

            else:
                if key == key_tuple[3]:
                    if not isinstance(value, datetime.date):
                        raise ValueError(
                            error_line[2].format(key=key))

                if key == key_tuple[5]:
                    if not isinstance(value, int):
                        raise ValueError(
                            error_line[2].format(key=key))

        self.info = info

    def __str__(self):

        line = "{f} {i} {o} {date} {polis} {price:,} руб.".format(
            f=self.f,
            i=self.i,
            o=self.o,
            date=self.birthday.strftime("%d/%m/%Y"),
            polis=self.polis_type,
            price=self.polis_price)

        return line

    @classmethod
    def from_string(cls, str_value):
        cls.info = {}

        pattern_search = r"^\s*(?P<f>[а-яА-Я]+)" +\
            r"\s+(?P<i>[а-яА-Я]+)" +\
            r"\s+(?P<o>[а-яА-Я]+)" +\
            r"\s+(?P<day>\d+)" +\
            r"[\.\-\/](?P<month>\d+)" +\
            r"[\.\-\/](?P<year>\d+)" +\
            r"\s+(?P<polis_type>[а-яА-Я]+)" +\
            r"\s+(?P<polis_price>\d+[^.,])"

        include = False
        match = re.search(pattern_search, str_value)
        if match:
            for key, value in match.groupdict().items():
                if key in ("year", "day", "month"):
                    if not include:
                        year = match.group("year")
                        if len(year) == 2:
                            year = "19" + year

                        cls.info["birthday"] = datetime.date(
                            int(year),
                            int(match.group("month")),
                            int(match.group("day")))

                        include = True

                elif key == "polis_price":
                    cls.info[key] = int(value)

                else:
                    cls.info[key] = value.capitalize()
        else:
            raise ValueError("Не удалось получить информацию!")

        return Customer(cls.info)

    def __getattr__(self, key):
        if key in self.info:
            return self.info[key]
        raise AttributeError(key)
