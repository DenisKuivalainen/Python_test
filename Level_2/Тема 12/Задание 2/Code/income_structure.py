"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import csv
import numpy as np
import matplotlib.pyplot as plt


class IncomeStructure:
    """Класс IncomeStructure создает столбчатую диаграмму по
    структуре доходов северно-западного федерального округа
    """

    OKRUG = "Северо-Западный  федеральный округ"

    def __init__(self):
        """Инициализация класса
        Свойства:
            - self._data - информация о структуре доходов
            - self.fields - поля
        """
        self._data = []
        self.fields = tuple()

    def __str__(self):
        """Возвращает поля"""
        fields = ""
        for i in range(len(self.fields) - 1):
            fields += " {},".format(self.fields[i])
        fields += " {}".format(self.fields[-1])
        return "Поля: {}".format(fields)

    def load(self, filename):
        """Загружает информацию из файла"""
        with open(filename, "r", encoding="utf-8") as fh:
            readers = csv.reader(fh, delimiter=';')
            rows = list(readers)
        fields = rows[0]
        for row in rows[1:]:
            if row[0] == IncomeStructure.OKRUG:
                dct = {fields[w]: float(row[w].replace(",", "."))
                       for w in range(2, len(row))}
                dct[fields[1]] = row[1]
                self._data.append(dct)
        self.fields = tuple(fields[1:])

    def _make_plot(self):
        """Генерирует изображение, не отображая его"""
        tick_label = [i[self.fields[0]] for i in self._data]

        ind = np.arange(len(tick_label))
        data = []
        for k in range(1, len(self.fields)):
            data.append([i[self.fields[k]] for i in self._data])
            data[k-1].append(self.fields[k])
        data.sort(key=lambda x: x[0])

        height = 0.35
        p1 = plt.barh(ind, data[0][:-1], height, color="red")
        p2 = plt.barh(ind, data[1][:-1], height, left=data[0][:-1],
                      color="orange")
        p3 = plt.barh(ind, data[2][:-1], height, left=data[1][:-1],
                      color="yellow")
        p4 = plt.barh(ind, data[3][0:-1], height, left=data[2][0:-1],
                      color="green")
        p5 = plt.barh(ind, data[4][0:-1], height, left=data[3][0:-1],
                      color="blue")

        plt.title("Структура доходов по субъекту РФ '{}'".
                  format(IncomeStructure.OKRUG))
        plt.yticks(ind, tick_label)
        plt.xticks(np.arange(0, 100, 10))
        plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0]), [i[-1] for i in data])
        plt.subplots_adjust(left=0.3, bottom=0.1, right=0.9, top=0.85)

    def show_plot(self):
        """Создать изображение и показать его на экране."""
        self._make_plot()
        plt.show()
