import logging
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    logging.info('Sending email to: ' + to)
    msg = Message(current_app.config['CRM_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=current_app.config['CRM_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
    logging.info('Email sent to: ' + to)