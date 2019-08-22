"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""


class Пицца:

    def __init__(self):
        self.название = "Заготовка"
        self.тесто = "тонкое"
        self.соус = "кечтуп"
        self.начинка = []

        self.цена = 0

    def __str__(self):
        subline = ""
        for начинка in self.начинка:
            subline += начинка + ", "
        subline = subline[:-2]
        line = "Пицца: {name} | Цена: {price:.2f} р."
        line += "\n   Тесто: {testo} Соус: {sous} "
        line += "\n   Начинка: {nachinka}"
        line = line.format(
            name=self.название,
            price=self.цена,
            testo=self.тесто,
            sous=self.соус,
            nachinka=subline)
        return line

    def подготовить(self):

        subline = ""
        for начинка in self.начинка:
            subline += начинка + ", "
        subline = subline[:-2]
        line = "Начинаю готовить пиццу {name}\n"
        line += "     - замешиваю {testo} тесто...\n"
        line += "     - добавляю соус: {sous}...\n"
        line += "     - и, конечно: {nachinka}..."
        line = line.format(
            name=self.название,
            testo=self.тесто,
            sous=self.соус,
            nachinka=subline)
        print(line)

    def испечь(self):
        print("Выпекаю пиццу... Готово!")

    def нарезать(self):
        print("Нарезаю на аппетитные кусочки...")

    def упаковать(self):
        print("Упаковываю в фирменную упаковку и готово!")


class ПиццаПепперони(Пицца):
    def __init__(self):
        super().__init__()

        self.название = "Пепперони"
        self.тесто = "тонкое"
        self.соус = "томатный"
        self.начинка = ["пепперони", "сыр моцарелла"]

        self.цена = 350


class ПиццаБарбекю(Пицца):

    def __init__(self):
        super().__init__()

        self.название = "Барбекю"
        self.тесто = "тонкое"
        self.соус = "барбекю"
        self.начинка = ["бекон", "ветчина", "зелень", "сыр моцарелла"]

        self.цена = 450


class ПиццаДарыМоря(Пицца):

    def __init__(self):
        super().__init__()

        self.название = "Дары моря "
        self.тесто = "пышное"
        self.соус = "тар-тар"
        self.начинка = ["кальмары", "креветки", "мидии", "сыр моцарелла"]

        self.цена = 550
