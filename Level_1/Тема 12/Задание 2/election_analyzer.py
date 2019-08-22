"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import csv
import matplotlib.pyplot as plt


class ElectionAnalyzer:
    """Класс ElectionAnalyzer выполняет:
      - формирование итогового списка партий с подсчетом голосов;
      - построение круговой диаграммы суммарного количества голосов.

    Поля:
      - self._data: двумерный массив данных вида:
             [[1, 'Партия 5', 1, 1, 2, 0.06666666666666667],
              [2, 'Партия 4', 2, 2, 4, 0.13333333333333333],
              [3, 'Партия 3', 3, 3, 6, 0.2]]

    Методы:
      - self.load(): загрузка, определение показателей и сортировка данных;
      - self._make_plot(): формирование изображения;
      - self.show_plot(): отображение изображения.
    """

    def __init__(self):
        self._data = list()

    def __str__(self):
        line = "Результаты ({len_data}):\n".format(len_data=len(self._data)-1)
        pattern_line = "{index:}. {name} {persent:.2f}%\n"
        for index, party in enumerate(self._data):
            if index == 0:
                continue
            line += pattern_line.format(
                index=index,
                name=party[1],
                persent=party[-1]*100)

        return line[:-1]

    def load(self, filename):
        parties = []
        with open(filename, encoding="utf-8") as fl:
            data_parties = csv.reader(fl)
            for line in data_parties:
                for index, element in enumerate(line):
                    if element.isdigit():
                        line[index] = int(element)
                parties.append(line)
        name_row = parties[0]
        parties = parties[1:]

        all_voises = sum(list(map(
            lambda party: sum(party[2:]), parties)))
        for party in parties:
            party.append(sum(party[2:]))
            party.append((party[-1])/all_voises)

        self._data = sorted(
            parties,
            key=lambda party: party[-1],
            reverse=True)

        self._data.insert(0, name_row)

    def _make_plot(self):

        assert not(self._data is None) and len(self._data) > 0, \
            "Отсутсвуют данные!"

        title_line = "Выборы в Государственную думу (2016): Результаты"
        fig, ax = plt.subplots()
        fig.canvas.set_window_title(title_line)
        ax.set_title(title_line)

        values = []
        labels = []
        for index, party in enumerate(self._data):
            if index == 0:
                continue
            line = "{name} ({persent:.2f}%)".format(
                name=party[1],
                persent=party[-1]*100)
            values.append(party[-2])
            labels.append(line)

        ax.pie(values, explode=[0.2] * len(values))
        ax.legend(loc="upper right")

        ax.set_position([0.2, 0.1, 1.5, 0.8])
        plt.legend(labels, bbox_to_anchor=(1., 0.8))
        ax.set_aspect("equal")
        fig.tight_layout()

        return fig

    def show_plot(self):
        self._make_plot()
        plt.show()
