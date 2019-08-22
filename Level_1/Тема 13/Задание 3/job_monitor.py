"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import time

from mailer import Mailer
from hh import Hh
from reporter import Reporter
import utils


class JobMonitor:
    """Класс JobMonitor реализует помощник кадрового менеджера.

    Поля:
      - self.mailer (mailer.Mailer);
      - self.hh (hh.Hh);
      - self.reporter (reporter.Reporter).
    """

    def __init__(self):
        self.mailer = Mailer()
        self.hh = Hh()
        self.reporter = Reporter()

    def __str__(self):
        return "JobMonitor v 0.1"

    def run(self, timeout):
        sec_old = None
        while True:
            sec_new = time.perf_counter()
            if sec_old is None or sec_new - sec_old > timeout:
                utils.log("Проверяю...")

                requests = self.mailer.check_requests()
                utils.log("Найдено новых запросов: {}".format(len(requests)))

                for i, request in enumerate(requests, start=1):
                    utils.log("Обработка запроса №{}: {}".format(i, request))

                    vacancies = self.hh.search(
                        title=request['title'],
                        area=request['area'],
                        experience=request['experience'],
                        salary=request['salary'])
                    utils.log("Найдено вакансий: {}".format(len(vacancies)))
                    for vacancy in vacancies:
                        utils.log(vacancy)

                    filename = self.reporter.make(request, vacancies)
                    utils.log("Документ \"{}\" сформирован".format(filename))

                    self.mailer.send_mail(request, filename)
                    utils.log("Письмо отправлено!")

                sec_old = sec_new
            else:
                utils.log("Ожидаю.")
                time.sleep(5)
                self.mailer.noop()
