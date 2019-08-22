"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from vk import VK

if __name__ == "__main__":
    try:
        user = int(174882525)
        token = "edef488cb08c818ee4659e666dacee4ee1fc93bede991609b5fd7fb9c89f2d111a0177241779406c14bc8"
        v = VK(user, token)
        print(v)
        v.show_plot()
    except Exception as err:
        print("Во время работы произошла ошибка: ", err)
