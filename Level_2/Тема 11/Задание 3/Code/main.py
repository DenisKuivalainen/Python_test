"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from backup_manager import Backup

if __name__ == "__main__":
    try:
        proj = input("Введите название проекта: ")
        bk = Backup(proj)
    except Exception as err:
        print("Во время работы произошла ошибка: ", err)
