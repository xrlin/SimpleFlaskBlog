# -*- coding : utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))    # 获取当前文件夹绝对路径

DEBUG = False

SSL = True

# config categories
CATEGORIES = ["Technology", "About"]
# configuration page num
PER_PAGE = 10

# configuration mysql
#SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s" % ('user1', '123456', '127.0.0.1', 'blog')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "date.sqlite")
WHOOSH_BASE = os.path.join(basedir, "whoosh_base")   # 设定全文搜索的数据库
# mail configureation
MAIL_USE_SSL = True
MAIL_SERVER = 'xx'
MAIL_PORT = 465
MAIL_USERNAME = 'xx'
MAIL_PASSWORD = 'xx'
MAIL_DEFAULT_SENDER = 'xx'     # 默认的sender

SUBJECT_HEADER = "来自xrlin的验证信息"     # 邮件标题
REPLY_SUBJECT_HEADER = "您在xrlin's blog的评论收到回复"  # 用作回复提醒的邮件标题

# 发送验证信息时的地址
token_url_template = "http://127.0.0.1:5000/auth/confirm/{0}"

BASE_URL = "http://127.0.0.1:5000/"

# mail body html
MAIL_BODY_HTML = "<p><b>您好:</b></p>" \
                 "<p>这是一封来自Xrlin's Blog的用户注册验证邮件，请点击以下链接进行验证</p><p>{0}</p> " \
                 "<p>from Xrlin's Blog</p>"

# 回复提醒
REPLY_MAIL_BODY_HTML = "<p><b>您好:</b></p>" \
                 "{0} 回复了您在 {1} 的评论" \
                 "<p>Send from Xrlin's Blog</p>"


SECRET_KEY = 'xxxxx'

UPLOAD_FOLDER = './static/upload/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

RECAPTCHA_PUBLIC_KEY = '6Ld4rwITAAAAAKUD5AntlHi7HL36W2vHJQOIjQmA'
RECAPTCHA_PRIVATE_KEY = '6Ld4rwITAAAAAFE8nTS852QbsqCBx1mN8D4BqenE'

# 管理员帐号名， 为配置方便暂时将管理员用户名写在配置文件
Admin = "xx"
