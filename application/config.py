#coding=utf-8
# -*- coding : utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))    # 获取当前文件夹绝对路径

# set debug to False when you publish the website in public
DEBUG = False

# set this to true to redirect all the request with https
SSL = True

# config categories in your blog
CATEGORIES = ["Technology", "About"]

# configuration page num per pagination
PER_PAGE = 10

# config database
# uncomment the line according which database you used, sqlite is the
# default database
# mysql
# SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s" % ('user1', '123456', '127.0.0.1', 'blog')
# sqlite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "date.sqlite")
# comment this because whoosh cannot support python3 now
# WHOOSH_BASE = os.path.join(basedir, "whoosh_base")   # 设定全文搜索的数据库
# mail configureation
# setting the mail info according your mail provider
# all mail config are get from system env var.
MAIL_USE_SSL = True
# Just for example, change this to adjust your mail server
MAIL_SERVER = 'smtp.qq.com'  
MAIL_PORT = 465
# Get mail account and password from system env, of course you can define those directly
MAIL_USERNAME = os.environ.get('BLOG_MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('BLOG_MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = MAIL_USERNAME   # default email sender

SUBJECT_HEADER = "来自xrlin的验证信息"     # subject_header 
REPLY_SUBJECT_HEADER = "您在xrlin's blog的评论收到回复"  # reply mail subject header

# change this url to your real domain and port
BASE_URL = "http://127.0.0.1:5000"

# a url with token to confirm information
token_url_template = BASE_URL + "/auth/confirm/{0}"

# mail's body html
MAIL_BODY_HTML = "<p><b>您好:</b></p>" \
                 "<p>这是一封来自Xrlin's Blog的用户注册验证邮件，请点击以下链接进行验证</p><p>{0}</p> " \
                 "<p>from Xrlin's Blog</p>"

# reply mail's body
REPLY_MAIL_BODY_HTML = "<p><b>您好:</b></p>" \
                 "{0} 回复了您在 {1} 的评论" \
                 "<p>Send from Xrlin's Blog</p>"


SECRET_KEY = 'xxxxx'

UPLOAD_FOLDER = './static/upload/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

RECAPTCHA_PUBLIC_KEY = '6Ld4rwITAAAAAKUD5AntlHi7HL36W2vHJQOIjQmA'
RECAPTCHA_PRIVATE_KEY = '6Ld4rwITAAAAAFE8nTS852QbsqCBx1mN8D4BqenE'

# define a super user for this website, this user must have registered in this website
# Get admin user's name from system env, this user must have registered in this website
Admin = os.environ.get('BLOG_ADMIN')
