import json
import smtplib
import ssl
from enum import IntEnum

import requests

from configuration import Configuration


class ConsoleOutputMode(IntEnum):
    NONE = 0
    PRETTY_CHANGES = 1
    JSON_ALL = 2


class Notifier:
    config = None

    def __init__(self, config: Configuration):
        self.config = config

    def notify(self, message, subject, noten):
        if int(self.config.getDefault('consoleOutputMode')) == int(ConsoleOutputMode.JSON_ALL):
            print(json.dumps(noten))
        elif int(self.config.getDefault('consoleOutputMode')) == int(ConsoleOutputMode.PRETTY_CHANGES):
            print(subject)
            print(message)

        if self.config.getDefault('mailSmtpHost') != '':
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(self.config.getDefault('mailSmtpHost'), self.config.getDefault('mailSSLPort'), context=context) as server:
                server.login(self.config.getDefault('mailLoginUser'), self.config.getDefault('mailLoginPassword'))
                server.sendmail(self.config.getDefault('mailSenderMail'), self.config.getDefault('mailReceiverMail'),
                                "Subject: " + subject + "\n\n" + message)

        if self.config.getDefault('telegramChatId') != '':
            send_text = 'https://api.telegram.org/bot' + self.config.getDefault('telegramBotToken') + '/sendMessage?chat_id=' \
                        + self.config.getDefault('telegramChatId') + '&parse_mode=Markdown&text=' + '**' + subject + '**' + message
            requests.get(send_text)
