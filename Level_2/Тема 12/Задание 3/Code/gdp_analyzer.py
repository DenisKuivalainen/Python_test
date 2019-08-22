"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import csv
import json
import matplotlib.pyplot as plt


class GDPAnalyzer:
    """Класс GDPAnalyzer отображает статистику ВВП по странам"""

    SETTFILE = "options.json"

    def __init__(self):
        """Инициализация класса
        Свойства:
            - self._settings - данные из файла настроек
            - self._data - данные о ВВП
        """
        self._settings = {}
        self._data = []
        self.fields = tuple()

        self._load_settings()

    def __str__(self):
        """Возвращает поля"""
        return "Поля: {}".format(self.fields)

    def _load_settings(self):
        """Загружает днные из файла настроек"""
        try:
            with open(GDPAnalyzer.SETTFILE, "r", encoding="utf-8") as fh:
                self._settings = json.loads(fh.read())
        except Exception as err:
            raise Exception("При получении данных из файла настроек "
                            "произошла ошибка: ", err)

    def load_data(self, filename):
        """Получает данные из файла с данными по ВВП"""
        with open(filename, "r", encoding="utf-8") as fh:
            readers = csv.reader(fh, delimiter=',')
            rows = list(readers)
        self.fields = rows[0]
        for row in rows[1:]:
            dct = {int(self.fields[w]): float(row[w])
                   for w in range(4, len(row)) if row[w]}
            dct[self.fields[0]] = row[0]
            dct[self.fields[1]] = row[1]
            dct[self.fields[2]] = row[2]
            dct[self.fields[2]] = row[3]
            self._data.append(dct)

    def _get_country(self, country):
        """Возвращает данные о ВВП в стране"""
        for i in self._data:
            if i["Country Name"] == country:
                return i

    def _get_dinamica_vvp(self):
        """Возращает динамику изменения ВВП по странам"""
        assert len(self._data) > 0, "Нет данных для анализа"

        dct = {}
        period = self._settings["plot"]["period"]
        countries = self._settings["plot"]["countries"]
        for country in countries:
            statistic = self._get_country(country)
            dct[country] = {}
            dct[country]["year"] = []
            dct[country]["vvp"] = []
            for year in range(period[0], period[1]+1):
                dct[country]["year"].append(year)
                dct[country]["vvp"].append(statistic[year])
        return dct

    def _last_year(self, dct):
        """Возвращает ВВП за последний доступный год"""
        for year in range(2016, 1960, -1):
            if dct.get(year):
                return dct.get(year)

    def _get_raspred_vvp(self):
        """Возвращает распределение ВВП по странам за
        последний доступный год
        """
        vvp = []
        for i in self._data:
            year = self._last_year(i)
            if year:
                vvp.append(year)
        return vvp

    def _get_unite_vvp(self):
        """Возвращает распределение ВВП между странами экономического союза"""
        dct = {}
        countries = self._settings["pie"]["countries"]
        for country in countries:
            statistic = self._get_country(country)
            year = self._last_year(statistic)
            if year:
                dct[country] = year
        return dct

    def _stats1(self, data, ax):
        """Генерирует график динамики изменения ВВП"""
        for i in data:
            year = data[i]["year"]
            vvp = data[i]["vvp"]
            ax.set_title("Динамика изменения ВВП")
            ax.set_xlabel("Год")
            ax.set_ylabel("ВВП")
            ax.plot(year, vvp, linewidth=2, label=i)
        ax.legend(loc="lower right")

    def _stats2(self, data, ax):
        """Генерирует гистограмму распределения ВВП между странами"""
        ax.set_title("Распределение ВВП между всеми странами")
        ax.set_xlabel("ВВП")
        ax.set_ylabel("Доля")
        bins = self._settings["hist"]["bins"]
        n, bins, patches = ax.hist(data, bins=bins,
                                   color="red", edgecolor="black")

    def _stats3(self, data, ax):
        """Генерирует круговую диаграмму распределения ВВП между
        странами экономического союза
        """
        unite = self._settings["pie"]["name"]
        ax.set_title("Распределение ВВП между странами '{}'".format(unite))
        values = list(data.values())
        labels = list(data.keys())

        ax.pie(values, labels=labels, autopct="%.1f%%", radius=1)
        ax.set_aspect("equal")

    def _make_plot(self):
        """Генерирует изображение, не отображая его"""
        assert len(self._data) > 0, "Нет данных для анализа"

        fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(12, 6))

        title = "ВВП стран мира"
        fig.canvas.set_window_title(title)
        fig.suptitle(title)

        self._stats1(self._get_dinamica_vvp(), ax1)
        self._stats2(self._get_raspred_vvp(), ax2)
        self._stats3(self._get_unite_vvp(), ax3)

        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85,
                            wspace=0.2, hspace=0.45)
        return fig

    def show_plot(self):
        """Создать изображение и показать его на экране."""
        self._make_plot()
        plt.show()
