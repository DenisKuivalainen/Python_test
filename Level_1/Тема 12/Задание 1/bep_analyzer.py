"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import math
import matplotlib
import matplotlib.pyplot as plt


class BepAnalyzer:
    """Класс BepAnalyzer выполняет:
      - поиск точки безубыточности;
      - построение графика безубыточности.

    Поля:
      - self._data: список словарей данных. Каждый словарь имеет ключи:
          - "bep_x": точка безубыточности (x);
          - "bep_y": точка безубыточности (y);
          - "fc": постоянные издержки;
          - "ic": себестоимость единицы продукции;
          - "price": цена единицы продукции,

    Методы:
      - self.find_bep(): определение точки безубыточности;
      - self.add_data(): добавление данных для анализа;
      - self.clear_data(): очистка данных для анализа;
      - self._make_plot(): формирование изображения;
      - self.show_plot(): вывод изображения.
    """

    def __init__(self):
        self._data = []

    def __str__(self):

        line = "Анализируемые данные ({len_data}):\n".format(
                                                len_data=len(self._data))
        pattern_line = "{index}.\n" \
            "  - bep_x: {bep_x}\n" \
            "  - bep_y: {bep_y}\n" \
            "  - fc: {fc}\n" \
            "  - ic: {ic}\n" \
            "  - price: {price}\n"
        for i, data in enumerate(self._data):
            line += pattern_line.format(
                    index=i + 1,
                    bep_x=data["bep_x"],
                    bep_y=data["bep_y"],
                    fc=data["fc"],
                    ic=data["ic"],
                    price=data["price"])

        return line[:-1]

    def find_bep(self, ic, fc, price):

        assert isinstance(ic, (int, float)) and ic > 0, "Не корретные данные!"
        assert isinstance(fc, (int, float)) and fc > 0, "Не корретные данные!"
        assert isinstance(price, (int, float)) and price > ic, \
            "Не корретные данные!"

        # Из-за округляния, теряется корректность второго графика,
        # но это необходимо, чтобы совпал вывод через __str__
        bep_x = int(math.ceil(fc / (price - ic)))
        bep_y = bep_x * price

        return {"bep_x": bep_x, "bep_y": bep_y}

    def add_data(self, ic, fc, price):

        assert isinstance(ic, (int, float)) and ic > 0, "Не корретные данные!"
        assert isinstance(fc, (int, float)) and fc > 0, "Не корретные данные!"
        assert isinstance(price, (int, float)) and price > ic, \
            "Не корретные данные!"

        data = {
            "ic": ic,
            "fc": fc,
            "price": price}
        data.update(self.find_bep(**data))

        self._data.append(data)

    def clear_data(self):
        self._data = []

    def _make_plot(self):
        assert not(self._data is None) and len(self._data) > 0, \
            "Отсутсвуют данные!"

        matplotlib.rc("font", family="Arial")
        fig, ax = plt.subplots(ncols=len(self._data))
        fig.canvas.set_window_title("Графики безубыточности")

        for i, data in enumerate(self._data):

            line = "График безубыточности при цене = {price:.2f}р.".format(
                                                    price=data["price"])
            ax[i].set_title(line)
            ax[i].set_xlabel("Шт.")
            ax[i].set_ylabel("руб.")

            x = list(range(0, int(data["bep_x"] * 2 + 1), 1))
            tr = list(map(lambda x: x * data["price"], x))
            fc = [data["fc"]] * len(x)
            vc = list(map(lambda x: x * data["ic"], x))
            tc = list(map(lambda x: data["fc"] + data["ic"] * x, x))

            ax[i].plot(
                [data["bep_x"]] * len(tr),
                tr,
                color="black",
                linewidth=1,
                linestyle="dashed")
            ax[i].plot(
                x,
                [data["bep_y"]] * len(x),
                color="black",
                linewidth=1,
                linestyle="dashed")

            ax[i].plot(
                x,
                tr,
                color="blue",
                linewidth=1,
                label="Валовой доход (TR)")
            ax[i].plot(
                x,
                fc,
                color="yellow",
                linewidth=1,
                label="Постоянные издержки (FC)")
            ax[i].plot(
                x,
                vc,
                color="green",
                linewidth=1,
                label="Переменные издержки (VC)")
            ax[i].plot(
                x,
                tc,
                color="red",
                linewidth=1,
                label="Валовые издержки (TC)",
                marker="o",
                markersize=3)

            ax[i].annotate(
                "Точка\n" +
                "безубыточности\n" +
                r"BEP=$\frac{FC}{P-AVC}$" +
                "\n({bep_x}, {bep_y})".format(
                                    bep_x=data["bep_x"],
                                    bep_y=data["bep_y"]),
                xy=(data["bep_x"], data["bep_y"]),
                xytext=(0, (x[-1] * data["price"] * 80) / 100),
                arrowprops=dict(arrowstyle='->'))
            ax[i].legend(loc="upper right")

        return fig

    def show_plot(self):
        self._make_plot()
        plt.show()
