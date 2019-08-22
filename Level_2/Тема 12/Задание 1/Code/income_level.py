"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import csv
import matplotlib.pyplot as plt
import statistics


class IncomeLevel:
    """Класс IncomeLevel создает круговую и столбчатую диаграммы по доходам
    по федеральным округам и субъектам северно-западного федерального округа
    """

    OKRUG = "Северо-Западный  федеральный округ"

    def __init__(self):
        """Инициализация класса
        Свойства:
            - self._okrug - информация о федеральных округах
            - self._subject - информация о субъектах в округе
        """
        self._okrug = []
        self._subject = []

    def __str__(self):
        """Возвращает информацию о доходах"""
        stroka = "Средний доход по федеральным округам РФ\n"
        for i in range(len(self._okrug)):
            stroka += "{0}. {1:37} {2:.2f} руб.\n".\
                      format(i+1, self._okrug[i][0]+" -", self._okrug[i][1])
        stroka += "\nДоход по округу '{}':".format(IncomeLevel.OKRUG)
        for i in range(len(self._subject)):
            stroka += "\n{0}. {1:23} {2} руб.".\
                      format(i+1, self._subject[i][0]+" -",
                             self._subject[i][1])
        return stroka

    def load(self, filename):
        """Загружает информацию из файла"""
        with open(filename, "r", encoding="utf-8") as fh:
            readers = csv.reader(fh, delimiter=';')
            rows = list(readers)
        okrug = rows[1][0]
        lst = []
        lst.append(okrug)
        for i in rows[1:]:
            if i[0] == okrug:
                lst.append(int(i[2]))
            else:
                self._okrug.append([lst[0], statistics.mean(lst[1:])])
                lst = []
                lst.append(i[0])
                lst.append(int(i[2]))
                okrug = i[0]
            if okrug == IncomeLevel.OKRUG:
                self._subject.append([i[1], int(i[2])])
        self._okrug.sort(key=lambda x: x[1], reverse=True)
        self._subject.sort(key=lambda x: x[1], reverse=True)

    def _make_plot(self):
        """Генерирует изображение, не отображая его"""
        assert len(self._okrug) > 0, "Нет данных для вывода!"
        assert len(self._subject) > 0, "Нет данных для вывода!"

        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(15, 6))

        fig.canvas.set_window_title("Уровень денежных доходов населения РФ")
        ax1.set_title("Средний доход по федеральным округам РФ")

        values = [i[1] for i in self._okrug]
        labels = ["{}. {} - {:.2f}".format(i+1, self._okrug[i][0],
                                           self._okrug[i][1])
                  for i in range(len(self._okrug))]

        ax1.pie(values, radius=1.2)
        ax1.legend(labels, loc='upper right', bbox_to_anchor=(1, 0.))
        ax1.set_position([0, 0.3, 0.5, 0.6])
        ax1.set_aspect("equal")

        ax2.set_title("Доход по округу '{}':".format(IncomeLevel.OKRUG))
        ax2.set_xlabel("Тыс. руб")
        tick_label = [i[0] for i in self._subject]
        size = [i[1] for i in self._subject]
        nums = [x + 1 for x in range(len(size))]
        ax2.barh(nums, size, tick_label=tick_label)
        return fig

    def show_plot(self):
        """Создать изображение и показать его на экране."""
        self._make_plot()
        plt.show()
