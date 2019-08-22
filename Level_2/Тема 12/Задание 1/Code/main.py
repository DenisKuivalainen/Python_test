"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from income_level import IncomeLevel

if __name__ == "__main__":
    il = IncomeLevel()
    try:
        il.load(filename="data_2017-12-27.csv")
        print(il)
        il.show_plot()
    except Exception as err:
        print("Во время работы приложения произошла ошибка:", err)
