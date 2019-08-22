"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from game import Game

if __name__ == "__main__":
    try:
        g = Game()
        g.run()
    except Exception as err:
        print("Во время работы произошла ошибка: ", err)
