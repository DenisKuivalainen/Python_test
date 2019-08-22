"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""


class Roman:
    ARABIC_MIN = 1
    ARABIC_MAX = 3999
    ROMAN_MIN = "I"
    ROMAN_MAX = "MMMCMXCIX"

    LETTERS = ["M", "CM", "D", "CD", "C", "XC", "L",
               "XL", "X", "IX", "V", "IV", "I"]
    NUMBERS = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]

    def __init__(self, value):
        if not isinstance(value, (int, str)):
            raise TypeError("Не могу создать римское число из {0}".
                            format(type(value)))

        if isinstance(value, int):
            self.__check_arabic(value)
            self._arabic = value
        elif isinstance(value, str):
            self._arabic = self.to_arabic(value)

    def __add__(self, other):
        if isinstance(other, Roman):
            return Roman(self.arabic + other.arabic)
        elif isinstance(other, int):
            self._arabic += other
            return self
        else:
            raise TypeError("Не корректный тип!")

    def __sub__(self, other):
        if isinstance(other, Roman):
            return Roman(self.arabic - other.arabic)
        elif isinstance(other, int):
            self._arabic -= other
            return self
        else:
            raise TypeError("Не корректный тип!")

    def __mul__(self, other):
        if isinstance(other, Roman):
            return Roman(self.arabic * other.arabic)
        elif isinstance(other, int):
            self._arabic *= other
            return self
        else:
            raise TypeError("Не корректный тип!")

    def __floordiv__(self, other):
        if isinstance(other, Roman):
            return Roman(self.arabic // other.arabic)
        elif isinstance(other, int):
            self._arabic //= other
            return self
        else:
            raise TypeError("Не корректный тип!")

    def __truediv__(self, other):
        return self.__floordiv__(other)

    def __str__(self):
        return Roman.to_roman(self._arabic)

    @staticmethod
    def __check_arabic(value):
        if value < Roman.ARABIC_MIN or value > Roman.ARABIC_MAX:
            raise ValueError("Число не принадлежит [{}; {}]".format(
                Roman.ARABIC_MIN, Roman.ARABIC_MAX))

    @staticmethod
    def __check_roman(value):
        for letter in value:
            if not(letter in Roman.LETTERS):
                raise ValueError("\'value\' содержит недопустимые символы!")

    @property
    def arabic(self):
        return self._arabic

    @staticmethod
    def to_arabic(roman):
        def letter_to_number(letter):
            i = Roman.LETTERS.index(letter)
            return Roman.NUMBERS[i]

        Roman.__check_roman(roman)

        i = 0
        value = 0

        while i < len(roman):

            number = letter_to_number(roman[i])

            i += 1

            if i == len(roman):
                value += number
            else:
                next_number = letter_to_number(roman[i])
                if next_number > number:
                    value += next_number - number
                    i += 1
                else:
                    value += number

        Roman.__check_arabic(value)
        return value

    @staticmethod
    def to_roman(arabic):
        Roman.__check_arabic(arabic)

        roman = ""
        n = arabic

        for i, number in enumerate(Roman.NUMBERS):
            while n >= number:
                roman += Roman.LETTERS[i]
                n -= Roman.NUMBERS[i]

        return roman
