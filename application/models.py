#coding=utf-8
from functools import reduce
from werkzeug.security import generate_password_hash, check_password_hash
__author__ = 'archer'

from flask import current_app
from flask_sqlalchemy import BaseQuery
from itsdangerous import JSONWebSignatureSerializer
from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import hashlib


class UserQuery(BaseQuery):

    def get_user_by_id(self, id):
        return self.get(id)

    def get_user_by_name(self, name):
        return self.filter(User.username.ilike(name)).first()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    query_class = UserQuery
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))       # 加密后的密码hash值
    confirmed = db.Column(db.Boolean, default=False)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User %s>" % self.username

    # 生成一个校验注册的信息，默认失效时间3600秒
    def generate_confirmation_token(self):
        s = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.id})

    # 校验验证信息
    def confirm(self, token):
        s = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    # 生成重置密码的token
    def generate_reset_token(self):
        s = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset': self.id})

    # 验证重置密码token
    def confirm_reset_token(self, token):
        s = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        return True

    def generate_change_email_token(self, new_email):
        s = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('id') != self.id:
            return False
        if data.get('new_email') is None:
            return False
        self.email = data.get('new_email')
        self.save()
        return True

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

'''
    目录model
'''


class Category(db.Model):

    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    articles = db.relationship('Article', backref='category', lazy='dynamic')

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "<Category %s>" % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

'''
    为了进行多对多表映射创建的映射辅助表
'''
article_tag_table = db.Table('article_tags', db.Model.metadata, db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
                             db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class ArticleQuery(BaseQuery):

    def search(self, keywords):

        allpage = []
        for key in keywords.split(','):
            allpage.append(db.or_(Article.title.contains(key), Article.context.contains(key)))
        p = reduce(db.and_, allpage)

        return self.filter(p)

'''
    博客文章
'''


class Article(db.Model):

    __tablename__ = 'articles'
    query_class = ArticleQuery
    # __searchable__ = ['title', 'context']   # 设定搜索范围
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    context = db.Column(db.Text(), nullable=False)
    created_date = db.Column(db.DateTime(), default=datetime.utcnow())
    view_count = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    tags = db.relationship('Tag', secondary=article_tag_table, backref='articles')
    comments = db.relationship('Comment', backref='article')    # 设置为dynamic不利于获取评论数

    def __init__(self, title=None, context=None, category_id=None, tags=[]):
        self.title = title
        self.context = context
        self.category_id = category_id
        self.tags = tags


    def __str__(self):
        return '<Article %s>' % self.title

    def save(self):
        db.session.add(self)
        db.session.commit()


class Tag(db.Model):

    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)


    def __init__(self, name=None):    # because flask-admin cannot pass arguments when create the model
        self.name = name

    def __str__(self):
        return "<Tag %s>" % self.name


class Comment(db.Model):
    """Class containing comments to a post"""

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reply_date = db.Column(db.DateTime())
    body = db.Column(db.String(255))

    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    children = db.relationship("Comment")

    def __init__(self, user_id, body, article_id, parent_id=None, reply_date=datetime.utcnow()):
        self.body = body
        self.article_id = article_id
        self.parent_id = parent_id
        self.user_id = user_id
        self.reply_date = reply_date

    def __str__(self):
        return "<Comment %s>" % self.body

    def save(self):
        db.session.add(self)
        db.session.commit()

# 为了使用flask-login扩展必须有一个用来加载对象的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
