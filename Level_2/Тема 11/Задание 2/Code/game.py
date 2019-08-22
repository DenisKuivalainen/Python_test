"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import sys
import datetime
import re


class Game:
    """Класс Game реализует логику игры.

    Методы:
      - run(): запуск игры;
      - _...: дополнительные методы.
    """

    MSG_GAME_TITLE = "Добро пожаловать в игру 'Угадай число'!"
    MSG_GAME_TIME = "Время начала игры: {}"
    MSG_GAME_RULE = "Правила довольно просты: Вы загадываете любое число"\
                    " я отгадываю.\nИтак, начнем. Загадывайте."\
                    " Как загадаете нажмите Enter."
    MSD_GAME_INTERVAL = "Отлично. Теперь через пробел введите границы"\
                        " интервала, в котором\nнаходится Ваше число: "
    MSG_GAME_BEGAN = "Теперь я попытаюсь отгадать Ваше число. Если я"\
                     " отгадаю его,\nвведите '+' или 'да', в противном "\
                     "случае введите что-либо другое."
    MSG_GAME_CHISLO = "Вы загадали число {}? - "
    MSG_GAME_END = "Игра закончена. Время окончания: {}"
    MSG_GAME_POP = "Количество попыток: {}"
    MSG_CHECK_INTERVAL = "Ошибка! Попробуйте еще раз. "
    MSG_GAME_OVER = "В интервале закончились числа. " + MSG_GAME_END

    FILENAME = "data.txt"
    GAME = r"Игра №\d{1,3}"  # шаблон для определения номера игры

    def _get_interval(self):
        """Запрашивает параметры игры: интервал, в котором находится число"""

        cmd_params = False
        if len(sys.argv) == 3:
            try:
                begin, end = int(sys.argv[1]), \
                                             int(sys.argv[2])
                cmd_params = True
            except Exception:
                # При отсутствии параметров командной строки
                pass

        print(Game.MSD_GAME_INTERVAL, end="")
        while True:
            try:
                if cmd_params:
                    print(begin, end, "(аргументы командной строки)")
                    cmd_params = False
                else:
                    params = input()
                    begin, end = map(int, params.split())

                assert self._can_run(begin, end)
                break
            except (AssertionError, ValueError):
                print(Game.MSG_CHECK_INTERVAL, end="")
            except Exception:
                raise
        return begin, end

    def _can_run(self, begin, end):
        """Проверяет интервал"""
        return begin < end

    def run(self):
        """Начать новую игру.

        Ход игры:
        1. Узнать интервал.
        2. Запустить игру.
        3. Показать результат.
        """
        print(Game.MSG_GAME_TITLE)
        input(Game.MSG_GAME_RULE)
        begin, end = self._get_interval()

        print(Game.MSG_GAME_BEGAN)
        time_begin = datetime.datetime.now()
        print(Game.MSG_GAME_TIME.format(time_begin))

        chislo = Chislo(begin, end)
        while(chislo.check_chislo()):  # пока число не вышло за интервал
            ch = input(Game.MSG_GAME_CHISLO.format(chislo.get_chislo()))
            if ch in ["+", "Да", "да"]:
                fl = 0
                break
            if not chislo.check_chislo():
                fl = 1
                break
        time_end = datetime.datetime.now()

        if fl:  # вывод сообщения в зависимости от результата игры
            print(Game.MSG_GAME_OVER.format(time_end))
        else:
            print(Game.MSG_GAME_END.format(time_end))

        kol = chislo.kol
        print(Game.MSG_GAME_POP.format(kol))

        self._save_rezultat(time_begin, time_end, kol)

    def _save_rezultat(self, time_begin, time_end, kol):
        """Сохраняет результат игры в файл txt"""
        nomer = self._get_n_game()
        with open(Game.FILENAME, "a", encoding="utf-8") as fh:
            fh.write("Игра №{}\n".format(nomer))
            fh.write(" Начало игры: {}\n".format(time_begin))
            fh.write(" Конец игры: {}\n".format(time_end))
            fh.write(" Количество попыток: {}\n".format(kol))

    def _get_n_game(self):
        """Возвращает номер игры"""
        try:
            with open(Game.FILENAME, "r", encoding="utf-8") as fh:
                text = fh.read()
            lst = re.findall(Game.GAME, text)
            match = None
            match = re.search(r"\d{1,3}", lst[-1])
            if match:
                i = int(match.group(0))
                return i + 1
            else:
                raise
        except Exception:
            return 1


class Chislo:
    """Класс Chislo угадывает число"""

    def __init__(self, begin, end):
        """Инициализация класса
        self._begin (int) - начало интервала
        self._end (int) - конец интервала
        self._chislo (int) - число
        self._kol (int) - количество попыток
        """
        self._begin = begin
        self._chislo = begin
        self._end = end
        self._kol = 0

    def get_chislo(self):
        """Возвращает число и увеличивает количество попыток"""
        self._chislo = self._begin + self.kol
        self._kol += 1
        return self._chislo

    def check_chislo(self):
        """Проверяет выход числа за интервал"""
        return self._chislo < self._end

    @property
    def kol(self):
        """Возвращает количество попыток"""
        return self._kol
