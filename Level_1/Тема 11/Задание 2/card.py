"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

class Card:
    """Класс Card представляет игральную карту.

    Поля экземпляра класса:
      - self._value (int): значение карты;
      - self.is_face (bool): True, если карта лежит лицом вверх.

    Методы экземпляра класса:
      - self.turn_face(): переворачивает карту лицом вверх.
      - self.turn_back(): переворачивает карту рубашкой вверх.

    Атрибуты класса:
      - BACK (str): рубашка карты.

    Свойства:
      - value (int): значение карты (только для чтения).
    """

    BACK = "X"

    def __init__(self, value):
        assert isinstance(value, int), "Некорректное значение!"

        self._value = value
        self.is_face = False

    def __str__(self):
        if self.is_face:
            return str(self._value)
        else:
            return Card.BACK

    def turn_face(self):
        self.is_face = True

    def turn_back(self):
        self.is_face = False

    @property
    def value(self):
        return self._value
