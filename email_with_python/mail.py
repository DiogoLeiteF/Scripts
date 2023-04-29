from base64 import encode
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
from time import sleep


def send_mail(some_thing, mails):
    ''' send email'''

    html = Template(Path('index.html').read_text(encoding='utf8'))
    email = EmailMessage()
    email['from'] = 'Leite Faria'
    email['to'] = mails
    email['subject'] = 'Thanks for your purchase.'

    email.set_content(html.substitute(name=some_thing), 'html')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('dummypc001@gmail.com', 'djqzmfnwtfvyzrdo')
        smtp.send_message(email)
        print('all good boss!')


emails = ['diogoleitefaria@gmail.com',
          'dummypc1@protonmail.com', 'silentroom10000@gmail.com']

for mail in emails:
    mail_split = mail.split('@')
    name = mail_split[0]
    send_mail(name, mail)
    sleep(10)
