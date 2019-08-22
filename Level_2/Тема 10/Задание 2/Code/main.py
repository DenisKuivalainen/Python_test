"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from complex_list import ComplexList
from cmplx import Complex
import random

if __name__ == "__main__":
    cl = ComplexList()
    for i in range(10):
        cl.add(Complex(random.randint(-50, 50), random.randint(-50, 50)))
    print(cl)
    cl.remove(1)
    cl.remove(2)
    print("Список комплексных чисел после удаления 2 эл.:\n", cl)
    print("Срез [1:5:1]:\n", cl[1:5:1])
    print("Элемент списка: ", cl[3])
    cl.save("data.json")
    cl1 = ComplexList()
    cl1.load("data.json")
    print("Загруженный список:\n", cl1)
