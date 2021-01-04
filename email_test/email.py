
import smtplib

import email

from email.mime.image import MIMEImage

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart, MIMEBase

from common.utils import hash_md5

SMTP_CONF = dict()


class EmailProcessor(object):
    """
    創建一個email處理器
    """
    def __init__(self):
        self._users = dict()
        self._smtp = 'smtp.'
        self._pop3 = 'pop.'

    def smtp_login(self, host, port, username, password):
        smtp_host = self._smtp + host

    def user_login(self, host, port, username, password):
        """"""
        try:
            smtp_obj = smtplib.SMTP(host, port)
            user_id = hash_md5(username)
            smtp_obj.login(username, password)
            self._users[user_id] = dict()
            self._users[user_id]["smtp_obj"] = smtp_obj
        except Exception as error:
            pass
