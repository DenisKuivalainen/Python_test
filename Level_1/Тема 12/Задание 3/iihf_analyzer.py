"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import csv
import datetime
import calendar
import locale
import matplotlib.pyplot as plt
import numpy as np


class IihfAnalyzer:
    """Класс IihfAnalyzer выполняет:
      - формирование итогового списка партий с подсчетом голосов;
      - построение круговой диаграммы суммарного количества голосов.

    Поля:
      - self._data: список словарей вида:

        [
            {'cohort': 1976, 'position': 'Защитник', 'country': 'RUS',
             'birth': datetime.datetime(1976, 5, 18, 0, 0),
             'bmi': 24.5434623813002, 'year': 2001,
             'club': 'anaheim mighty ducks', 'age': 24.952772073922,
             'side': 'L', 'height': 185.0, 'name': 'tverdovsky oleg',
             'no': 10, 'weight': 84.0},
            ...
        ]

      - self.fields (tuple): данные о хоккеистах (по возрастанию):
          ('age', 'birth', 'bmi', 'club', 'cohort', 'country', 'height',
           'name', 'no', 'position', 'side', 'weight', 'year')

      - self.years (tuple): годы проведения ЧМ (по возрастанию):
          (2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
           2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016)

      - self.countries (tuple): страны-участники ЧМ (по возрастанию):
          ('AUT', 'BLR', 'CAN', 'CZE', 'DEN', 'FIN',
           'FRA', 'GER', 'HUN', 'ITA', 'JPN', 'KAZ', 'LAT', 'NOR', 'POL',
           'RUS', 'SLO', 'SUI', 'SVK', 'SWE', 'UKR', 'USA')

    """

    PLAYER_POSITION_NAME = {
      "G": "Вратарь", "D": "Защитник", "F": "Нападающий"
    }

    def __init__(self):
        self._data = list()
        self.fields = tuple()
        self.years = tuple()
        self.countries = tuple()

    def __str__(self):
        line_fields = str(self.fields)
        line_fields = line_fields[1:]
        line_fields = line_fields[:-1]
        line_fields = line_fields.replace("'", "")

        line = "Набор данных ({count_players}):\n" \
               " - поля: {fields};\n" \
               " - годы: {years};\n" \
               " - страны-участники: {countries}.".format(
                count_players=len(self._data),
                fields=line_fields,
                years=self.years,
                countries=self.countries)

        return line

    def load(self, filename):


        with open(filename, encoding="utf-8") as fl:
            hockey_players = csv.DictReader(fl, delimiter=",")
            for player in hockey_players:
                player['cohort'] = int(player['cohort'])
                player['position'] = \
                    IihfAnalyzer.PLAYER_POSITION_NAME[player['position']]
                birth_line = player['birth'].split("-")
                player['birth'] = datetime.datetime(
                    int(birth_line[0]),
                    int(birth_line[1]),
                    int(birth_line[2]),
                    0,
                    0)
                player['bmi'] = float(player['bmi'])
                player['year'] = int(player['year'])
                player['age'] = float(player['age'])
                player['height'] = float(player['height'])
                player['no'] = int(player['no'])
                player['weight'] = float(player['weight'])
                self._data.append(player)

        fields = set(self._data[0].keys())
        years = set()
        countries = set()
        for player in self._data:
            years.add(player['year'])
            countries.add(player['country'])

        self.fields = tuple(sorted(fields))
        self.years = tuple(sorted(years))
        self.countries = tuple(sorted(countries))

    def _get_player_id(self, player):

        return (
            player['name'],
            player['birth'],
            player['country'],
            player['position'])

    def _get_players_without_dublicates(self, data):
        set_players = set(map(
            lambda player: self._get_player_id(player), data))

        list_dict_players = list()
        for player in set_players:
            list_dict_players.append({
                'name': player[0],
                'birth': player[1],
                'country': player[2],
                'position': player[3]})

        return list_dict_players

    def get_wc_participation_stats(self):

        assert len(self._data) > 0, "Нет данных для анализа"

        dict_players = dict()
        for player in self._data:
            id_player = self._get_player_id(player)
            if id_player in dict_players.keys():
                dict_players[id_player] += 1
            else:
                dict_players[id_player] = 1

        return dict_players

    def get_trend_data(self):

        assert len(self._data) > 0, "Нет данных для анализа"

        dict_trend_players = dict()
        for position in self.PLAYER_POSITION_NAME.values():
            dict_trend_players[position] = {'x': list(), 'y': list()}
        for player in self._data:
            dict_trend_players[player['position']]['x'].append(player['year'])
            dict_trend_players[player['position']]['y'].append(
                player['height'])

        return dict_trend_players

    def get_birthday_month_stats(self):

        assert len(self._data) > 0, "Нет данных для анализа"

        birthday_month_dict = dict()
        players = self._get_players_without_dublicates(self._data)
        for player in players:
            if player['birth'].month in birthday_month_dict.keys():
                birthday_month_dict[player['birth'].month] += 1
            else:
                birthday_month_dict[player['birth'].month] = 1

        return birthday_month_dict

    def get_position_stats(self):

        assert len(self._data) > 0, "Нет данных для анализа"

        position_stats_dict = dict()
        players = self._get_players_without_dublicates(self._data)
        for player in players:
            if player['position'] in position_stats_dict.keys():
                position_stats_dict[player['position']] += 1
            else:
                position_stats_dict[player['position']] = 1

        return position_stats_dict

    def _make_plot(self):
        assert len(self._data) > 0, "Нет данных для анализа"

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(ncols=2, nrows=2,
                                                     figsize=(12, 6))

        title = "Хоккейная статистика ЧМ: " + str(self.years)
        fig.canvas.set_window_title(title)
        fig.suptitle(title)

        self._stats1(self.get_wc_participation_stats(), ax1)
        self._stats2(self.get_trend_data(), ax2)

        self._stats3(self.get_birthday_month_stats(), ax3)
        self._stats4(self.get_position_stats(), ax4)

        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85,
                            wspace=0.2, hspace=0.45)

        return fig

    def _stats1(self, data, ax):
        labels = []
        list_value = list(data.values())

        for value in list_value:
            if not(value in labels):
                labels.append(value)
        labels = sorted(labels)

        bins = len(labels) - 1

        n, bins, patches = ax.hist(
            list_value,
            bins=bins,
            normed=True,
            color="red",
            edgecolor="black")

        ax.set_title("Распределение хоккеистов по количеству участий в ЧМ")
        ax.set_xlabel("Количество ЧМ")
        ax.set_ylabel("Доля")
        ax.set_xticks([x + 0.5 for x in bins])
        ax.set_xticklabels(labels)

    def _stats2(self, data, ax):
        x_trend, y_trend = dict(), dict()
        for key, value in data.items():
            x_trend[key] = value['x']
            y_trend[key] = np.poly1d(np.polyfit(value['x'], value['y'], 1))

        labels_and_color = {
            'Вратарь': "blue",
            'Защитник': "orange",
            'Нападающий': "green"}

        for label, color in labels_and_color.items():
            ax.plot(
                x_trend[label],
                y_trend[label](x_trend[label]),
                color=color,
                linewidth=1,
                linestyle="dashed",
                label=label)

        ax.set_title("Тренды изменения роста игрока для каждой позиции")
        ax.set_xlabel("Год ЧМ")
        ax.set_ylabel("Рост (см.)")
        ax.legend(loc="lower right")

    def _stats3(self, data, ax):
        locale.setlocale(locale.LC_ALL, "Russian")

        x = list(data.keys())
        y = list(data.values())
        labels = list(calendar.month_abbr)[1:]

        ax.set_title("Распределение хоккеистов по месяцам рождения")
        ax.bar(x, y, tick_label=labels)
        ax.set_ylabel("чел.")

    def _stats4(self, data, ax):
        labels = ['Нападающий', 'Защитник', 'Вратарь']
        pozition = [data[labels[0]], data[labels[1]], data[labels[2]]]

        ax.pie(pozition, labels=labels, autopct='%1.1f%%')
        ax.set_title("Распределение позиций между хоккеистами")
        ax.axis('equal')

    def show_plot(self):
        self._make_plot()
        plt.show()
