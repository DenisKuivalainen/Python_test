"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from тс import ТранспортноеСредство
from тс import ВодноеТС
from тс import КолесноеТС
from тс import Автомобиль


if __name__ == "__main__":

    try:
        тс = [ТранспортноеСредство(), ВодноеТС(), КолесноеТС(), Автомобиль()]
        print("Классы программы:\n")
        for i in тс:
            print(" - {}\n".format(type(i)))
        for i in тс:
            print(i)
            print("\nВызываю метод 'ехать()':")
            i.ехать()
            print("\n")

        print("Для классов КолесноеТС() и Автомобиль():")
        for i in тс[2:]:
            print("Вызываю метод 'заправить(100)':")
            i.заправить(100)
            print("\nВызываю метод 'ехать()'")
            i.ехать()
            print("\n")
    except Exception as err:
        print("Во время работы приложения произошла ошибка! ", err)
