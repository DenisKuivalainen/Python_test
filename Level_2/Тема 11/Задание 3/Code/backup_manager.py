"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import os.path
import sys
import shutil
import json
import datetime


class Backup:
    """Класс Backup выполняет резервное копирование файлов"""

    SETTFILE = "settings.json"

    def __init__(self, proj):
        """Инициализация класса
        Свойства:
            - self._proj (str) - название проекта
            - self._log_name (str) - имя файла для логирования
            - self._folders (list) - пути бекапа
            - self._tree (list) - дерево директорий
            - self._settings (dict) - настройки программы
            - self._log (dict) - данные для логирования:
                                 errors - ошибки при работе программы,
                                 begin_date - дата начала копирования,
                                 end_date - дата конца копирования,
                                 files - скопированные файлы
        """
        assert isinstance(proj, str), "Название должно быть типа 'str'!"
        self._proj = proj
        self._log_name = ""
        self._folders = []
        self._tree = []
        self._settings = {}
        self._log = {"errors": [],
                     "begin_date": None,
                     "end_date": None,
                     "files": []}
        self._run()

    def __str__(self):
        """Возвращает настройки программы"""
        text = "{0:12} {1}\n".format("Проект:", self._proj)
        text += "Список папок:\n"
        for i in self._folders:
            for key, value in i.items():
                text += "  {0:10} {1}\n".format(key+":", value)
        text += "Опции:"
        for key, value in self._settings.items():
            text += "\n  {0:10} {1}".format(key+":", value)
        return text

    def str_tree(self):
        """Возвращает строковое представление дерева директорий"""
        text = "Содержимое директорий:"
        sp = 0
        for folders in self._tree:
            for i in folders:
                text += "\n" + i
                for dr, prop in folders[i].items():
                    text += "\n  {}: {}".format(prop["path"],
                                                self._get_prop(prop["size"],
                                                               sp))
        return text

    def _get_prop(self, prop, sp):
        """Рекурсивная функция, фозвращает строковое представление
        ветки дерева
        Параметры:
            - prop - содержимое элемента ([] или (int, float))
            - sp (int) - отступ
        """
        try:
            if isinstance(prop, (int, float)):  # если файл
                return " - {0:.2f} Кб".format(prop)
            elif isinstance(prop, list):  # если папка
                text = ""
                for i in prop:
                    for dr, prop in i.items():
                        s = " " * sp + "|" + "_" * sp
                        text += "\n  {2}{0} {1}".\
                                format(dr, self._get_prop(prop["size"], sp+3),
                                       s)
                return text
        except Exception as err:
            mesg = "  Ошибка: {}".format(err)
            self._log['errors'].append(mesg)
            print(mesg)

    def _get_settings(self):
        """Считывает настройки из settings.json"""
        try:
            with open(Backup.SETTFILE, "r", encoding="utf-8") as fh:
                data = json.loads(fh.read())
            self._log_name = data["log_filename"]

            assert data["projects"].get(self._proj, None),\
                "В файле настроек отсутствует проект '{}'!".format(self._proj)

            self._folders = data["projects"][self._proj]["folders"]
            self._settings = data["projects"][self._proj]["options"]
            self._check_settings()
        except Exception as err:
            raise Exception(err)

    def _check_settings(self):
        """Проверяет поле options"""
        if self._settings.get("size_max", None):
            assert isinstance(self._settings["size_max"], int),\
                "В файле настроек значение секции 'size_max' не типа 'int'!"
        assert self._settings.get("confirm", 'None') != 'None',\
            "В файле настроек отсутствует секция 'confirm'!"
        assert isinstance(self._settings["confirm"], bool),\
            "В файле настроек значение секции 'confirm' не типа 'bool'!"

    def _run(self):
        """Работа программы"""
        try:
            self._get_settings()  # получение данных настроек
            print(self.__str__())  # вывод настроек

            for i in self._folders:  # создание дерева файлов
                data = dict()
                for key, value in i.items():
                    data[key] = self._get_tree(value)
                self._tree.append(data)

            print(self.str_tree())  # вывод дерева
            self._backup()  # бекап
            self._log['end_date'] = datetime.datetime.now()
        except Exception as err:
            mesg = "  Ошибка: {}".format(err)
            self._log['errors'].append(mesg)
            print(mesg)
        finally:
            if self._log:
                self._save_log()

    def _get_tree(self, value):
        """Рекурсивная функция, получает дерево файлов
        Параметры:
            - value (str) - путь
        Результат:
            {<Имя>:{path:<путь>,
                    size:<[содержимое папки] или
                         <размер файла(int,float)>>}}
        """
        path = os.path.normpath(value)
        data = dict()
        try:
            if self._check_dir(path):  # если папка
                dirname = os.path.split(path)
                data[dirname[1]] = {"path": path}
                files = os.listdir(path)  # получаем содержимое папки

                # заполнение данных о содержимом папки
                data[dirname[1]]["size"] =\
                    [self._get_tree(os.path.join(path, filename))
                     for filename in files]

            elif self._check_file(path):  #
                filename = os.path.split(path)
                # получение данных о файле
                data[filename[1]] = self._get_file(filename[1], path)
            else:
                # если не файл и не папка
                data[path] = {"path": path, "size": None}
                raise OSError("Дирректория {} не найдена".format(path))

        except OSError as err:
            mesg = "  OSError: {}".format(err)
            self._log['errors'].append(mesg)
            print(mesg)
        except Exception as err:
            mesg = "  Ошибка: {}".format(err)
            self._log['errors'].append(mesg)
            print(mesg)
        finally:
            return data

    def _get_file(self, filename, path):
        """Возвращает данные о файле"""
        size = os.path.getsize(path) / 1024
        return {"path": path, "size": size}

    def _check_dir(self, path):
        """Проверяет, является ли элемент в пути path папкой"""
        return os.path.isdir(path)

    def _check_file(self, path):
        """Проверяет, является ли элемент в пути path файлом"""
        return os.path.isfile(path)

    def _backup(self):
        """Выполняет бекап файлов"""
        self._log['begin_date'] = datetime.datetime.now()

        for i in range(len(self._folders)):
            try:
                f1 = self._check_dir(self._folders[i]["dest"])
                f2 = self._check_dir(self._folders[i]["src"])
                if f1 and f2:
                    # если пути существуют выполняется бекап
                    for dr, prop in self._tree[i]["src"].items():
                        self._copy(prop, self._folders[i]["dest"])
                else:
                    raise OSError("Не могу скопировать файлы из {} в {},"
                                  " т.к. какого-то из путей не существует".
                                  format(self._folders[i]["src"],
                                         self._folders[i]["dest"]))
            except OSError as err:
                mesg = "  OSError: {}".format(err)
                self._log['errors'].append(mesg)
                print(mesg)
            except Exception as err:
                mesg = "  Ошибка: {}".format(err)
                self._log['errors'].append(mesg)
                print(mesg)

    def _copy(self, prop, dest):
        """Рекурсивная функция, выполняет копирование содержимого директории
        Параметры:
            - prop (dict) - свойства копируемой директории
            - dest (str) - путь, куда нужно копировать
        """
        if isinstance(prop["size"], (int, float)):  # если файл
            self._copy_file(prop, dest)
        elif isinstance(prop["size"], list):  # если папка
            try:
                dir_name = os.path.split(prop["path"])
                #  если в dest отсутствует папка - создает ее
                if not self._check_dir(dest + "/" + dir_name[1]):
                    os.mkdir(dest + "/" + dir_name[1])
                    print("Папка {} была создана!".format(dir_name[1]))
                #  копирует содержимое папки в dest
                for i in prop["size"]:
                    for dr, pr in i.items():
                        self._copy(pr, dest + "/" + dir_name[1])

            except Exception as err:
                mesg = "  Ошибка: {}".format(err)
                self._log['errors'].append(mesg)
                print(mesg)

    def _copy_file(self, prop, dest):
        """Копирует файл
        Параметры:
            - prop (dict) - свойства файла
            - dest (str) - путь, куда нужно копировать
        """
        try:
            dir_name = os.path.split(prop["path"])
            assert self._check_file(prop["path"]),\
                "Файл {} не найден!".format(prop["path"])

            flag = True
            if self._settings.get("size_max"):
                if prop["size"] > self._settings["size_max"]:
                    mesg = "Файл {} превышает допустимый размер - {}кб!".\
                            format(prop["path"], self._settings["size_max"])

                    if self._settings["confirm"]:
                        answer = input("{}, скопировать его? (y/n) ".
                                       format(mesg)).upper()
                        if answer != "Y":
                            flag = False
                    else:
                        raise Exception(mesg)

            if self._check_file(dest + "/" + dir_name[1]):
                if self._settings["confirm"]:
                    answer = input("Файл {} уже существует, скопировать его?"
                                   " (y/n) ").upper()
                    if answer != "Y":
                        flag = False

            if flag:
                shutil.copy(prop["path"], dest)
                print("Файл {} скопирован!".format(prop["path"]))
                self._log['files'].append("{0} - {1:.2f}кб".
                                          format(prop["path"], prop["size"]))

        except Exception as err:
            mesg = "  Ошибка: {}".format(err)
            self._log['errors'].append(mesg)
            print(mesg)

    def _save_log(self):
        """Сохраняет результат выполнения программы"""
        try:
            with open(self._log_name, "w", encoding="utf-8") as fh:
                if self._tree:
                    fh.write(self.str_tree())
                fh.write("\n\nДата/время начала копирования: {}".
                         format(self._log['begin_date']))

                fh.write("\n\nДата/время конца копирования: {}".
                         format(self._log['end_date']))

                time = self._log['end_date'] - self._log['begin_date']
                fh.write("\n\nПрошло времени: {}".format(time))

                fh.write("\n\nСкопировано файлов: {}".
                         format(len(self._log['files'])))
                for line in self._log['files']:
                    fh.write("\n  " + line)

                fh.write("\n\nОшибки при выполнении программы {}:".
                         format(len(self._log['errors'])))
                for line in self._log['errors']:
                    fh.write("\n" + line)
        except Exception as err:
            print("При записи файла логов произошла ошибка: ", err)


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            proj = sys.argv[1]
        else:
            proj = input("Введите название проекта: ")
        bk = Backup(proj)
    except Exception as err:
        print("Во время работы произошла ошибка: ", err)
