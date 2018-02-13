from threading import Thread
from flask import render_template
from app import app, smtp
from flask_mailer import Email


def send_async_email(app, msg):
    with app.app_context():
        smtp.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Email(subject, from_addr=sender, to=recipients, text=text_body)
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Test] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
