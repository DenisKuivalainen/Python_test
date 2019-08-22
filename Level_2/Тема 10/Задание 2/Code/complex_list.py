"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from cmplx import Complex
import json


class ComplexList:
    """Класс ComplexList реализует работу со списком комплексных чисел."""

    def __init__(self):
        """
        Инициализация класса.
        Параметры:
            - self._complex (list) - список комплексных чисел
        """
        self._complex = list()

    def add(self, value):
        """Добавляет комплексное число в список"""

        assert isinstance(value, Complex),\
            "Тип добавляемого числа не Complex()!"
        self._complex.append(value)

    def remove(self, index):
        """Удаляет элемент из списка по индексу"""

        assert isinstance(index, int), "Тип переданного значения не int!"
        assert index < len(self._complex),\
            "Элемента под таким индексом не существует!"
        del self._complex[index]

    def __getitem__(self, k):
        """Возвращает срез элементов списка"""

        if isinstance(k, slice):
            lst = ComplexList()
            for i in self._complex[k.start: k.stop: k.step]:
                if i:
                    lst.add(i)
            return lst
        else:
            assert isinstance(k, int),\
                "Тип переданного значения не int!"
            assert k < len(self._complex),\
                "Элемента под таким индексом не существует!"
            return self._complex[k]

    def __len__(self):
        """Возвращает азмер списка"""

        return len(self._complex)

    def __str__(self):
        """Возвращает строковое представление класса"""

        string = "Список комплексных чисел ({}):".format(len(self._complex))
        for i in range(len(self._complex)):
            string += "\n{}. {}".format(i+1, self._complex[i])
        return string

    def save(self, filename="data.json"):
        """Сохраняет комплексные числа в json файл"""

        lst = filename.split(".")
        assert lst[-1] == "json", "Формат файла не json"
        data = []
        for i in range(len(self._complex)):
            data.append({"real": self._complex[i].real,
                        "imaq": self._complex[i].imaq})
        with open(filename, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(data, ensure_ascii=False, indent=4))
        print("Файл успешно записан")

    def load(self, filename="data.json"):
        """Загружает комплексные числа из json файла"""

        lst = filename.split(".")
        assert lst[-1] == "json", "Формат файла не json"

        with open(filename, "r", encoding="utf-8") as fh:
            data = json.loads(fh.read())

        assert isinstance(data, list), "Загруженные данные не типа list!"
        for i in data:
            assert "real" in i.keys() and "imaq" in i.keys(),\
                "Загруженный файл не имеет нужных ключей!"
            self._complex.append(Complex(i["real"], i["imaq"]))
        print("Файд успешно прочитан")
