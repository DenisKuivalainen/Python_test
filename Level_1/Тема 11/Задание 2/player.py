"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""
from card_list import CardList


class Player:
    """Класс Player представляет игрока.

    Атрибуты экземпляра класса:
      - self.name (str): имя игрока;
      - self.card_list (CardList): выбранные карты игрока.

    Методы экземпляра класса:
      - add_card(): добавляет карту в выбранные;
      - make_choice(): возвращает индекс выбранной игроком карты.
    """

    def __init__(self, name):
        self.name = name
        self.card_list = CardList()

    def __str__(self):
        return self.name + " [" + str(self.card_list) + "] " + str(
            self.card_list.sum())

    def add_card(self, card):
        card.is_face = True
        self.card_list.append(card)

    def make_choice(self):
        return int(input())
