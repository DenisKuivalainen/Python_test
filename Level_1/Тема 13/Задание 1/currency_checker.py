"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import sys
import os.path
import re
import datetime
import time
import smtplib
from email.mime.text import MIMEText
import requests


NO_DATA = "Нет данных"


class CurrencyChecker:
    """Класс CurrencyChecker реализует валютный помощник.

    Поля:
        Данные ИТ-аккаунта (прописаны в коде)
        - self.it_email: e-mail ИТ-отдела;
        - self.it_email_password: пароль от e-mail ИТ-отдела;
        - self.it_email_smtp_server: SMTP-сервер для e-mail ИТ-отдела;
        - self.it_email_smtp_port: SMTP-порт для e-mail сервера ИТ-отдела;
        Данные руководителя
        - self.ceo_name: ФИО руководителя;
        - self.ceo_email: e-mail руководителя.
        Прочее
        - self.log_filename: имя файла для логгирования;
        - self.msg: письмо для отправки (email.mime.text).

    Методы:
      - self._log(): вывод события на экран и в лог-файл;
      - self.run(): бесконечный цикл работы - получение данных и их отправка;
      - self.get_info(): получение котировок с сайта;
      - self._create_message(): формирование текста сообщения для отправки.
    """

    def __init__(self, ceo_name, ceo_email):
        self.ceo_name = ceo_name
        self.ceo_email = ceo_email

        self.it_email =
        self.it_email_password =
        self.it_email_smtp_server = "smtp.gmail.com"
        self.it_email_smtp_port = 587

        app_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.log_filename = os.path.join(app_path, "log.txt")
        self.msg = ""

    def __str__(self):
        return "CurrencyChecker v 0.1"

    def _log(self, message):
        date = datetime.datetime.today()
        line = "{date} | {message}".format(
            date=date.strftime("%Y-%m-%d %X"),
            message=message)

        print(line)

        with open(self.log_filename, "a", encoding="utf-8") as fh:
            fh.write("\n"+line)

    def run(self, timeout, currencies):
        while True:
            try:
                info = self.get_info(currencies)
                self._log("Данные получены: " + str(sorted(info.items())))

                text = self._create_message(info)
                self.send_mail(text)
                self._log("Письмо успешно отправлено!")
            except Exception as err:
                self._log("Произошла ошибка: " + str(err))
            finally:
                time.sleep(timeout)

    @staticmethod
    def get_info(currencies):
            try:
                return float(value.replace(',', '.'))
            except ValueError:
                return NO_DATA

        res = dict()
        for currence in currencies:
            res[currence] = tuple()

        r = requests.get("http://www.finanz.ru/valyuty/v-realnom-vremeni-rub")

        for currence in res:
            reg_ex = \
                r"title=\"" + \
                "(?:{name}\/RUB)".format(name=currence) + \
                r"(?:(?:.+\n){3}.+>)" + \
                r"(?P<value>\d+,\d+)" + \
                r"(?:(?:.+\n){3}.+>)" + \
                r"(?P<time>\d+:\d+:\d+)"

            match = re.search(reg_ex, r.text)
            if match:
                match_dict = match.groupdict()
                res[currence] = (
                    _value_to_float(match_dict["value"]),
                    match_dict["time"])
            else:
                res[currence] = (NO_DATA, NO_DATA)

        return res

    def _create_message(self, info):

        res = """\
{ceo_name}!

Обновленные курсы валют:
{info_str}

С уважением, ИТ-отдел.\
"""
        info_str = "\n"
        pattern_str = "  - {name}: {value} ({time})\n"
        for key, value in sorted(info.items()):
            info_str += pattern_str.format(
                name=key,
                value=value[0],
                time=value[1])

        return res.format(
            ceo_name=self.ceo_name,
            info_str=info_str[:-1])

    def send_mail(self, text):
        self.msg = MIMEText(text)
        data = datetime.datetime.today()
        self.msg["Subject"] = "Курсы валют на {date}".format(
            date=data.strftime("%Y-%d-%m %X"))
        self.msg["From"] = self.it_email
        self.msg["To"] = self.ceo_email

        server = smtplib.SMTP(
            self.it_email_smtp_server,
            self.it_email_smtp_port)
        try:
            server.starttls()
            server.login(self.it_email, self.it_email_password)
            server.send_message(self.msg)
        except Exception:
            raise
        finally:
            server.quit()
