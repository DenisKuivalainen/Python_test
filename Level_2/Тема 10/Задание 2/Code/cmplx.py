"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import math
import json


class Complex:
    """Класс Complex реализует работу с комплексными числами."""

    def __init__(self, real=0, imaq=0):
        """
        Инициализация класса.
        Параметры:
            - self.real (int, float) - действительная часть
            - self.imaq (int, float) - мнимая часть
        """

        if not self.check_complex(real, imaq):
            raise TypeError("Тип переданных параметров не 'int' или 'float'!")

        self.real = real
        self.imaq = imaq

    def __str__(self):
        """Вернуть строковое представление класса."""

        zn = ""
        if self.imaq >= 0:
            zn = "+"
        return "({}{}{}j)".format(self.real, zn, self.imaq)

    def __add__(self, other):
        """Создать новый объект как сумму self и other."""

        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imaq + other.imaq)
        else:
            raise TypeError("Число - {} не является Complex".
                            format(type(other)))

    def __sub__(self, other):
        """Создать новый объект как разность self и other."""

        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imaq - other.imaq)
        else:
            raise TypeError("Число - {} не является Complex".
                            format(type(other)))

    def __mul__(self, other):
        """Создать новый объект как произведение self и other."""

        if isinstance(other, Complex):
            real = self.real * other.real - self.imaq * other.imaq
            imaq = self.real * other.imaq + other.real * self.imaq
            return Complex(real, imaq)
        else:
            raise TypeError("Число - {} не является Complex".
                            format(type(other)))

    def __truediv__(self, other):
        """Создать новый объект как частное self и other."""
        if isinstance(other, Complex):
            dl = other.real**2 + other.imaq**2
            real = (self.real * other.real + self.imaq * other.imaq) / dl
            imaq = (other.real * self.imaq - self.real * other.imaq) / dl
            return Complex(real, imaq)
        else:
            raise TypeError("Число - {} не является Complex".
                            format(type(other)))

    def __abs__(self):
        """Возвращает модуль комплексного числа"""
        return self._abs()

    def __eq__(self, other):
        """Сравнивает два комплексных числа"""
        if isinstance(other, Complex):
            return self.real == other.real and self.imaq == other.imaq
        else:
            raise TypeError("Число - {} не является Complex".
                            format(type(other)))

    def _abs(self):
        """Считает модуль комплексного числа"""

        return (self.real**2 + self.imaq**2)**(1/2)

    def conjugate(self):
        """Создать новый объект как сопряжение self"""

        return Complex(self.real, -self.imaq)

    def __pow__(self, other):
        """Создать новый объект как self в степени other"""

        if isinstance(other, (int, float)):
            mod = self._abs()
            arg = math.atan(self.imaq / self.real)
            real = mod**other * math.cos(other * arg)
            imaq = mod**other * math.sin(other * arg)
            if isinstance(other, int) and other >= 0:
                real = math.floor(real)
                imaq = math.floor(imaq)
            return Complex(real, imaq)
        else:
            raise TypeError("Не могу возвести Complex число - {0}".
                            format(type(other)))

    @classmethod
    def from_string(cls, str_value):
        """Создать новый объект из строки str_value"""

        if not isinstance(str_value, str):
            raise TypeError("Переданное значение не 'str'!")

        try:
            char = str_value[0]
            if '-' in str_value[2:-1]:
                lst = str_value[1:].split('-')
                fl = 1
            elif '+' in str_value:
                lst = str_value[1:].split('+')
                fl = 0
            else:
                raise
            lst[0] = char + lst[0]
            if "." in lst[0]:
                real = float(lst[0])
            else:
                real = int(lst[0])
            if "." in lst[1]:
                imaq = float(lst[1][0:-1])
            else:
                imaq = int(lst[1][0:-1])

            if fl:
                imaq = -imaq
        except Exception:
            raise ValueError("Не удалось получить комплексное"
                             "число из строки - {}".format(str_value))
        return cls(real, imaq)

    @staticmethod
    def check_complex(real, imaq):
        """Проверяет типы переданных данных"""

        fl = 1
        if not isinstance(real, (int, float)):
            fl = 0
        if not isinstance(imaq, (int, float)):
            fl = 0
        return fl

    def save(self, filename="data.json"):
        """Сохраняет комплексное число в json файл"""

        lst = filename.split(".")
        assert lst[-1] == "json", "Формат файла не json"

        data = {"real": self.real,
                "imaq": self.imaq}
        with open(filename, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(data, ensure_ascii=False, indent=4))
        print("Файл успешно записан")

    def load(self, filename="data.json"):
        """Загружает комплексное число из json файла"""

        lst = filename.split(".")
        assert lst[-1] == "json", "Формат файла не json"
        with open(filename, "r", encoding="utf-8") as fh:
            data = json.loads(fh.read())
        assert isinstance(data, dict), "Загруженные данные не типа dict!"
        assert "real" in data.keys() and "imaq" in data.keys(),\
            "Загруженный словарь не имеет нужных ключей!"
        assert self.check_complex(data["real"], data["imaq"]),\
            "Тип переданных параметров не 'int' или 'float'!"
        self.real = data["real"]
        self.imaq = data["imaq"]
        print("Файл успешно прочитан")
