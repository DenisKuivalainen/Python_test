"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import json
import datetime
import re
import sys
import os.path


class Settings:
    """Класс Settings хранит настройки приложения.

    Атрибуты класса:
      - DATETIME_FORMAT - формат даты/времени;
      - DATETIME_REGEX - рег. выражение для идентификации даты/времени.

    Атрибуты экземпляра класса:
      - self._data - словарь настроек;
      - self.filename - имя файла настроек;

    Ключи в настройках:
      - "run_count": (int) - кол-во запусков;
      - "last_run_datetime": (datetime.datetime) - дата/время
                                                   последнего запуска;
      - "last_run_platform_info": (tuple) - информация о платформе
                                            последнего запуска.
    """
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATETIME_REGEX = "\d+-\d+-\d+\s\d+:\d+:\d+"

    def __init__(self):

        self._data = {}
        filename = os.path.split(sys.path[0])
        filename = os.path.split(filename[0])
        self.filename = os.path.join(filename[0], "tests", "settings.json")

    def __str__(self):
return self._data

    def set_value(self, name, value):

        if isinstance(value, datetime.datetime):
            self._data[name] = value.strftime(Settings.DATETIME_FORMAT)
        else:
            self._data[name] = value

    def get_value(self, name, default=None):

        try:
            value = self._data[name]
            if isinstance(value, str):
                match = re.search(Settings.DATETIME_REGEX, value)
                if match:
                    value = datetime.datetime.strptime(
                        match.string, Settings.DATETIME_FORMAT)
            return value
        except Exception:
            return default

    def load(self):
        try:
            with open(self.filename, "r") as fh:
                self._data = json.loads(fh.read())
        except Exception:
            self.save()

    def save(self):
        try:
            with open(self.filename, "w") as fh:
                fh.write(json.dumps(self._data, ensure_ascii=False, indent=4))
        except Exception:
            raise
