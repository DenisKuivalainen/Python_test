"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from gdp_analyzer import GDPAnalyzer

if __name__ == "__main__":
    gdp = GDPAnalyzer()
    try:
        gdp.load_data(filename="world_bank_gdp_data_2017-02-01.csv")
        print(gdp)
        gdp.show_plot()
    except Exception as err:
        print("Во время работы приложения произошла ошибка:", err)
