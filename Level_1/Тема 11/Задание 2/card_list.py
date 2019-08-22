"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import random
import functools
from card import Card


class CardList:
    """Класс CardList представляет набор карт
    (например, в руке у игрока или на столе).

    Поля экземпляра класса:
      - self._cards (list из Card): карты в наборе.

    Методы экземпляра класса:
      - self.shuffle(): перемешивает карты в наборе;
      - self.append(): добавляет карту в набор;
      - self.remove(): удаляет карту из набора;
      - self.pop(): удаляет и возвращает карту из набора;
      - self.is_empty(): True, если набор пустой;
      - self.sum(): считает сумму значения карт.
    """

    def __init__(self):
        self._cards = list()

    def __str__(self):
        return str(
                functools.reduce(
                    lambda line, subline: str(line) + " " + str(subline),
                    self._cards))

    def __len__(self):
        return len(self._cards)

    def shuffle(self):
        random.shuffle(self._cards)

    def append(self, card):
        assert isinstance(card, Card), "Это не карта!"

        self._cards.append(card)

    def pop(self, index):
        return self._cards.pop(index)

    def sum(self):
        return sum(list(map(lambda x: x.value, self._cards)))

    def is_empty(self):
        if len(self._cards) == 0:
            return True
        else:
            return False
