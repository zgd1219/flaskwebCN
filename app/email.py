from . import mail
from flask import render_template
from flask_mail import Message
from flask import current_app
from threading import Thread

# set FLASKY_ADMIN=anotherzgd@sina.cn
# set MAIL_USERNAME=anotherzgd@sina.cn
# set MAIL_PASSWORD=zgd1219

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    print(app.config['FLASKY_MAIL_SENDER'])
    print(to)
    print(app.config['MAIL_USERNAME'])
    print(app.config['MAIL_PASSWORD'])
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
