"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import sys
import os
import datetime

app_path = os.path.dirname(os.path.realpath(sys.argv[0]))
log_filename = os.path.join(app_path, "log.txt")

agency_name = "Python Test"


def log(message):

    date = datetime.datetime.today()
    line = "{date} | {message}"

    try:
        print(line.format(
            date=date.strftime("%Y-%m-%d %X"),
            message=message))
    except Exception:
        print(line.format(
            date=date.strftime("%Y-%m-%d %X"),
            message="Не удалось отобразить строку из-за" +
            " ошибки кодировки консоли."))

    with open(log_filename, "a", encoding="utf-8") as fh:
        fh.write("\n" + line.format(
            date=date.strftime("%Y-%m-%d %X"),
            message=message))
