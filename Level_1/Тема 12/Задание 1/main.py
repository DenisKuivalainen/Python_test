"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from bep_analyzer import BepAnalyzer

if __name__ == "__main__":

    ba = BepAnalyzer()
    try:
        ba.add_data(ic=200, fc=30000, price=250)
        ba.add_data(ic=200, fc=30000, price=1000)

        print(ba)

        ba.show_plot()
    except Exception as err:
        print("Во время работы приложения произошла ошибка:", err)
