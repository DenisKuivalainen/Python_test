"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import datetime
import platform
from settings import Settings


def get_last_run_info(settings, launch_dt):
    """
    Параметры:
      - settings: настройки - экземпляр класса Settings;
      - launch_dt (datetime.datetime): дата/время запуска программы.
    """
    run_count = settings.get_value("run_count", 0)
    if run_count != 0:
        last_run_seconds = round(
                    (launch_dt - settings.get_value(
                        "last_run_datetime")).total_seconds())
        last_run_platform_info = tuple(
                            settings.get_value("last_run_platform_info"))
    else:
        last_run_seconds = -1
        last_run_platform_info = tuple()

    return (run_count, last_run_seconds, last_run_platform_info)


def update_last_run_info(settings, launch_dt):
    """
      - settings: настройки - экземпляр класса Settings;
      - launch_dt (datetime.datetime): дата/время запуска программы.
    """
    settings.set_value("run_count", settings.get_value("run_count", 0) + 1)
    settings.set_value("last_run_datetime", launch_dt)
    settings.set_value("last_run_platform_info", tuple(platform.uname()))


if __name__ == "__main__":
    launch_dt = datetime.datetime.now()
    settings = Settings()
    try:
        settings.load()

        run_count, last_run_seconds, last_run_platform_info = \
            get_last_run_info(settings, launch_dt)

        print("Сейчас программа запущена: {}-й раз.".format(run_count + 1))
        if run_count > 0:
            print("С предыдущего запуска прошло {} с.".
                  format(last_run_seconds))
            print("Информация о платформе: {}".format(last_run_platform_info))

        update_last_run_info(settings, launch_dt)
        settings.save()
    except Exception as err:
        print("Во время работы приложения произошла ошибка:", err)
