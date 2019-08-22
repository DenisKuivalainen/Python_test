"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from iihf_analyzer import IihfAnalyzer

if __name__ == "__main__":

    analyzer = IihfAnalyzer()
    try:
        analyzer.load(filename="hockey_players.csv")
        print(analyzer)

        analyzer.show_plot()
    except Exception as err:
        print("Во время работы приложения произошла ошибка:", err)
