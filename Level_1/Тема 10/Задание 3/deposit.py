"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

class TimeDeposit:
    """Абстрактный класс - срочный вклад.

    https://ru.wikipedia.org/wiki/Срочный_вклад.

    Поля:
      - self.name (str): наименование;
      - self._interest_rate (float): процент по вкладу (0; 100];
      - self._period_limit (tuple (int, int)):
            допустимый срок вклада в месяцах [от; до);
      - self._sum_limit (tuple (float, float)):
            допустимая сумма вклада [от; до).
    Свойства:
      - self.currency (str): знак/наименование валюты.
    Методы:
      - self._check_self(initial_sum, period): проверяет соответствие данных
            ограничениям вклада;
      - self.get_profit(initial_sum, period): возвращает прибыль по вкладу;
      - self.get_sum(initial_sum, period):
            возвращает сумму по окончании вклада.
    """

    def __init__(self, name, interest_rate, period_limit, sum_limit):
        self.name = name
        self._interest_rate = interest_rate
        self._period_limit = period_limit
        self._sum_limit = sum_limit
        self._check_self()

    def __str__(self):

        number_list_str = list(self._sum_limit)
        for i, number_str in enumerate(number_list_str):
            number_str = str(number_str)
            new_line = ""
            while len(number_str) > 3:
                new_line += "," + number_str[len(number_str)-3:]
                number_str = number_str[:-3]
            number_str = number_str + new_line
            number_list_str[i] = number_str

        subline = "{0:<20}{1}\n"
        line = ""
        line += subline.format("Наименование:", self.name)
        line += subline.format("Валюта:", self.currency)
        line += subline.format("Процентная ставка:", self._interest_rate)
        line += subline.format(
                                "Срок (мес.):",
                                "[{}; {})".format(*self._period_limit))
        line += subline.format(
                                "Сумма:",
                                "[{}; {})".format(
                                                number_list_str[0],
                                                number_list_str[1]))

        return line[:-1]

    @property
    def currency(self):
        return "руб."

    def _check_self(self):
        assert 0 < self._interest_rate <= 100, \
            "Неверно указан процент по вкладу!"
        assert 1 <= self._period_limit[0] < self._period_limit[1], \
            "Неверно указаны ограничения по сроку вклада!"
        assert 0 < self._sum_limit[0] <= self._sum_limit[1], \
            "Неверно указаны ограничения по сумме вклада!"

    def _check_user_params(self, initial_sum, period):
        is_sum_ok = self._sum_limit[0] <= initial_sum < self._sum_limit[1]
        is_period_ok = self._period_limit[0] <= period < self._period_limit[1]
        assert is_sum_ok and is_period_ok, "Условия вклада не соблюдены!"

    def get_profit(self, initial_sum, period):
        self._check_user_params(initial_sum, period)
        return initial_sum * self._interest_rate / 100 * period / 12

    def get_sum(self, initial_sum, period):

        return initial_sum + self.get_profit(initial_sum, period)


class BonusTimeDeposit(TimeDeposit):

    def __init__(self, name, interest_rate, period_limit, sum_limit, bonus):
        self._bonus = bonus
        super().__init__(name, interest_rate, period_limit, sum_limit)

    def __str__(self):

        number_str = str(self._bonus["sum"])
        new_line = ""
        while len(number_str) > 3:
            new_line += "," + number_str[len(number_str)-3:]
            number_str = number_str[:-3]
        number_str = number_str + new_line

        subline = "{0:<20}{1}\n"
        line = super().__str__()
        line += "\n"
        line += subline.format("Бонус (%):", self._bonus["percent"])
        line += subline.format("Бонус (мин. сумма):", number_str)

        return line[:-1]

    def _check_self(self):

        super()._check_self()
        assert 0 < self._bonus["percent"] <= 100, \
            "Неверно указан процент по бонусу!"
        assert self._bonus["sum"] > 0, \
            "Неверно указаны ограничения по сумме бонуса!"

    def get_profit(self, initial_sum, period):
        summa = super().get_profit(initial_sum, period)
        if initial_sum >= self._bonus["sum"]:
            summa += summa * self._bonus["percent"] / 100

        return summa


class CompoundTimeDeposit(TimeDeposit):

    def __str__(self):
        subline = "{0:<20}{1}\n"
        line = super().__str__()
        line += "\n"
        line += subline.format("Капитализация %   :", "Да")

        return line[:-1]

    def get_profit(self, initial_sum, period):

        self._check_user_params(initial_sum, period)

        return initial_sum * (1 + self._interest_rate / 100 / 12) ** period \
            - initial_sum




deposits_data = dict(interest_rate=5, period_limit=(6, 18),
                     sum_limit=(1000, 100000))

deposits = (
    TimeDeposit("Сохраняй", interest_rate=5,
                period_limit=(6, 18),
                sum_limit=(1000, 100000)),
    BonusTimeDeposit("Бонусный 2", **deposits_data,
                     bonus=dict(percent=5, sum=2000)),
    CompoundTimeDeposit("С капитализацией", **deposits_data),
    TimeDeposit("Сохраняй 2", interest_rate=10,
                period_limit=(11, 24),
                sum_limit=(500, 10000)),
    BonusTimeDeposit("Бонусный 10", **deposits_data,
                     bonus=dict(percent=10, sum=1000)),
    CompoundTimeDeposit("С капитализацией 1", interest_rate=11,
                        period_limit=(1, 18),
                        sum_limit=(100, 10000))
)
