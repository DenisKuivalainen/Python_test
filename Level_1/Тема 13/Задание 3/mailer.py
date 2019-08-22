"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import sys
import re
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import decode_header

import utils


class Mailer:
    """Класс Mailer отвечает за чтение и отправку почты.

    Поля:
      - self.login (str): логин (email) почтового сервиса;
      - self.password (str): пароль для почтового сервиса;
      - self.imap_server (imaplib.IMAP4_SSL): объект - IMAP-сервер;
      - self.imap_server_url (str): адрес IMAP-сервера;
      - self.imap_port (int): порт IMAP-сервера;
      - self.smtp_server (smtplib.SMTP): объект - SMTP-сервер;
      - self.smtp_server_url (str): адрес SMTP-сервера;
      - self.smtp_port (int): порт SMTP-сервера;
      - self.msg (email.Message): электронное письмо.
    """

    def __init__(self):
        self.login =
        self.password =
        self.imap_server_url = "imap.gmail.com"
        self.imap_port = 993
        self.smtp_server_url = "smtp.gmail.com"
        self.smtp_port = 587

        self.imap_server = imaplib.IMAP4_SSL(
            self.imap_server_url,
            self.imap_port)
        self.imap_server.login(self.login, self.password)

        self.smtp_server = smtplib.SMTP(
            self.smtp_server_url,
            self.smtp_port)
        self.smtp_server.starttls()
        self.smtp_server.login(self.login, self.password)

        self.msg = None

    def __str__(self):
        return "Mailer v 0.1"

    def noop(self):
        self.imap_server.noop()
        self.smtp_server.noop()

    def disconnect(self):
        self.imap_server.quit()
        self.smtp_server.quit()

    @staticmethod
    def _get_request_info(message):
        text, encoding, mime = get_message_info(message)

        info = {
            'email': do_decode_header(message["From"]),
            'datetime': message["Date"],
            'subject': do_decode_header(message["Subject"]),
            'text': text,
            'title': None,
            'area': None,
            'experience': None,
            'salary': None}

        keys_dict = {
            'Поиск': 'title',
            'Регион': 'area',
            'Опыт работы (лет)': 'experience',
            'З/п (руб.)': 'salary'}

        pattern_regex = \
            r"^\s*(?P<name>[а-яА-Я\/\.\(\) ]+)" +\
            r":\s*" +\
            r"(?P<line>[a-zA-Zа-яА-Я0-9 -]+)"
        regex = re.compile(pattern_regex, flags=re.MULTILINE)
        match = regex.search(text)
        if match:
            for each_match in regex.finditer(text):
                if each_match.group('name') == "Поиск":
                    line = each_match.group('line').lower().split()
                    line = " ".join(list(map(lambda word:
                                    word.capitalize(), line)))
                    info[keys_dict[each_match.group('name')]] = \
                        line.strip()
                else:
                    info[keys_dict[each_match.group('name')]] = \
                        each_match.group('line').strip()
        else:
            return None

        if info['subject'] != "Просьба прислать актуальные вакансии":
            return None

        if not(info['title']) or not(info['area']):
            return None

        for key in ['experience', 'salary']:
            if info[key]:
                if info[key].isdigit():
                    digit = int(info[key])
                    if digit == 0:
                        info[key] = None
                    else:
                        info[key] = digit
                else:
                    info[key] = digit

        return info

    def check_requests(self):
        requests = []
        try:
            self.imap_server.select()

            response, messages_nums = self.imap_server.search(None, "(UNSEEN)")
            if response != "OK":
                raise imaplib.IMAP4.error("Не удалось получить список писем.")

            messages_nums = messages_nums[0].split()
            utils.log("Найдено новых писем: {}".format(len(messages_nums)))

            for message_num in reversed(messages_nums):
                response, data = \
                    self.imap_server.fetch(message_num,
                                           message_parts="(RFC822)")
                if response != "OK":
                    utils.log("Не удалось получить письмо №",
                              int(message_num.decode()))
                    continue

                self.imap_server.store(message_num, '-FLAGS', '\Seen')

                raw_message = data[0][1]
                self.msg = email.message_from_bytes(raw_message)

                info = Mailer._get_request_info(self.msg)
                if info:
                    info.update({"id": message_num})
                    requests.append(info)

            return requests
        except imaplib.IMAP4.error as err:
            utils.log("Возникла следующая ошибка:", err)
            raise

    def send_mail(self, info, filename):
        self.msg = MIMEMultipart()
        self.msg["Subject"] = info['subject']
        self.msg["From"] = self.login
        self.msg["To"] = info['email']

        text = "Здравствуйте!\n\n"          \
               "Ответ на Ваш запрос содержится во вложении\n\n"         \
               "С уважением, агентство \"{}\"".format(utils.agency_name)

        self.msg.attach(MIMEText(text, "plain"))

        with open(filename, "rb") as fh:
            attachment = MIMEApplication(fh.read())
        attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=filename)
        self.msg.attach(attachment)

        try:
            self.smtp_server.send_message(self.msg)

            self.imap_server.store(info['id'], '+FLAGS', '\Seen')
        except smtplib.SMTPException as err:
            utils.log("Возникла следующая ошибка:", err)
            raise


def do_decode_header(header):
    header_parts = decode_header(header)

    res = []
    for decoded_string, encoding in header_parts:
        if encoding:
            decoded_string = decoded_string.decode(encoding)
        elif isinstance(decoded_string, bytes):
            decoded_string = decoded_string.decode("ascii")
        res.append(decoded_string)

    return "".join(res)


def get_part_info(part):
    encoding = part.get_content_charset()
    if not encoding:
        encoding = sys.stdout.encoding
    mime = part.get_content_type()
    message = part.get_payload(decode=True).decode(encoding,
                                                   errors="ignore").strip()

    return message, encoding, mime


def get_message_info(message):
    message_text, encoding, mime = "Нет тела сообщения", "-", "-"

    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() in ("text/html", "text/plain"):
                message_text, encoding, mime = get_part_info(part)
                break
    else:
        message_text, encoding, mime = get_part_info(message)

    return message_text, encoding, mime
