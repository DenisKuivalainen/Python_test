"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""


import time


class Заказ:

    счетчик_заказов = 0

    def __init__(self):
        self.заказанные_пиццы = []
        Заказ.счетчик_заказов += 1

    def __str__(self):
        res = "Заказ №{index}\n".format(index=Заказ.счетчик_заказов)
        for i, пицца in enumerate(self.заказанные_пиццы):
            res += "{index}. ".format(index=i + 1)
            res += str(пицца)
            res += "\n"
        res += "Сумма заказа: {:.2f} р.".format(self.сумма())
        return res

    def добавить(self, пицца):
        self.заказанные_пиццы.append(пицца)

    def сумма(self):
        сумма = 0
        for пицца in self.заказанные_пиццы:
            сумма += пицца.цена

        return сумма

    def выполнить(self):
        print("\nЗаказ поступил на выполнение...")
        for i, пицца in enumerate(self.заказанные_пиццы):
            print("{index}. {name}".format(index=i + 1, name=пицца.название))
            пицца.подготовить()
            time.sleep(1)
            пицца.испечь()
            time.sleep(1)
            пицца.нарезать()
            time.sleep(1)
            пицца.упаковать()
            time.sleep(1)
            print("")
        print("Заказ №{index} готов! Приятного аппетита!".format(
            index=Заказ.счетчик_заказов))
