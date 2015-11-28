#coding=utf-8
from application import mail
from flask_mail import Message
from threading import Thread
from flask import current_app

__author__ = 'archer'


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

'''
    :subject  邮件标题
    ：recipents 包含收件人的列表
    : token_url 用来验证的链接
    : html_body 邮件正文
'''


def send_mail(subject, recipients, token_url):
    app = current_app._get_current_object()
    html_body=app.config['MAIL_BODY_HTML']
    msg = Message(subject, recipients=recipients)
    msg.html = html_body.format(token_url)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()


def send_reply_mail(subject, recipients, reply_user, article_url):
    app = current_app._get_current_object()
    html_body=app.config['REPLY_MAIL_BODY_HTML']
    msg = Message(subject, recipients=recipients)
    msg.html = html_body.format(reply_user, article_url)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
