from flask import current_app, render_template
from flask_mail import Mail, Message

mail = Mail()

def send_email(to, subject, template, **kwargs):
    msg = Message(
        subject=subject,
        recipients=[to],
        html=render_template(f'{template}.html', **kwargs)
    )
    mail.send(msg) 