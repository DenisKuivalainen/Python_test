"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from card import Card
from card_list import CardList
import options


class CardTable:
    """Класс CardTable представляет игорный стол.

    Умеет:
      - хранить карты, лежащие на столе;
      - "отдавать" карту;
      - определять - пуст или нет.

    Атрибуты экземпляра класса:
      - self._card_list (CardList): набор карт на столе.

    Методы экземпляра класса:
      - self.take_card(): берет карту со стола;
      - self.is_empty(): True, если на слоле нет карт.

    Свойства:
      - card_count (int): количество карт на столе.
    """

    def __init__(self, cards_count):
        assert cards_count > 1, "Недостаточное кол-во карт, для игры!"

        self._card_list = CardList()
        for i in range(1, cards_count + 1):
            card = Card(i)
            if options.debug:
                card.is_face = True
            self._card_list.append(card)
        self._card_list.shuffle()

    def __str__(self):
        line = "Карты на столе ({length}): {cards}".format(
                length=len(self._card_list),
                cards=self._card_list)
        return line

    def take_card(self, index):
        try:
            if 1 <= index:
                return self._card_list.pop(index-1)
            else:
                raise IndexError
        except IndexError:
            raise

    def is_empty(self):
        if self._card_list.is_empty():
            return True
        else:
            return False

    @property
    def card_count(self):
        return len(self._card_list)
