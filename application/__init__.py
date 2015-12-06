#coding=utf-8
# -*- coding : utf-8 -*-

from flask import Flask
from flask.ext.markdown import Markdown
from flask_admin import Admin
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_migrate import Migrate
from flask_gravatar import Gravatar
from . import config
bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = "auth.login"    # 设定未授权登录时跳转到的页面
pagedown = PageDown()   # 在线markdown编辑预览扩展
migrate = Migrate()
administrator = Admin(name="Admin", template_mode="bootstrap3")

from .auth import auth as auth_blueprint
from .main import main as main_blueprint
from .admin.views import  MicroBlogModelView, ArticleModelView
from .admin.views import ArticleModelView
from application.models import Article, User, Category, Tag

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    md = Markdown(app, extensions=['fenced_code'])
    gravatar = Gravatar(app, size=30,
                    rating='g',
                    default='mm',
                    force_default=False,
                    force_lower=False,
                    use_ssl=True,
                    base_url=None)
    pagedown.init_app(app)
    administrator.init_app(app)
    administrator.add_view(ArticleModelView(Article, db.session))
    administrator.add_view(MicroBlogModelView(User, db.session))
    administrator.add_view(MicroBlogModelView(Category, db.session))
    administrator.add_view(MicroBlogModelView(Tag, db.session))
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(main_blueprint)

    return app




