#coding=utf-8
# -*- coding : utf-8 -*-

from flask import Flask
from flask_admin import Admin
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_gravatar import Gravatar
from . import config
import misaka as m
import houdini as h
from misaka import HtmlRenderer
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = "auth.login"    # 设定未授权登录时跳转到的页面
migrate = Migrate()
administrator = Admin(name="Admin", template_mode="bootstrap3")

from .auth import auth as auth_blueprint
from .main import main as main_blueprint
from .admin.views import  MicroBlogModelView, ArticleModelView
from .admin.views import ArticleModelView
from application.models import Article, User, Category, Tag

class HighlightCodeRender(HtmlRenderer):
    def blockcode(self, text, lang):
        if not lang:
           return '\n<pre><code>%s</code></pre>\n' % \
               h.escape_html(text.strip())
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

render = HighlightCodeRender()
def transalte_markdown(text):
    md = m.Markdown(render, extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS | m.EXT_TABLES | m.EXT_AUTOLINK | m.EXT_SPACE_HEADERS | m.EXT_STRIKETHROUGH | m.EXT_SUPERSCRIPT)
    return md(text)

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    gravatar = Gravatar(app, size=30,
                    rating='g',
                    default='mm',
                    force_default=False,
                    force_lower=False,
                    use_ssl=True,
                    base_url=None)
    app.jinja_env.filters['markdown'] = transalte_markdown
    administrator.init_app(app)
    administrator.add_view(ArticleModelView(Article, db.session))
    administrator.add_view(MicroBlogModelView(User, db.session))
    administrator.add_view(MicroBlogModelView(Category, db.session))
    administrator.add_view(MicroBlogModelView(Tag, db.session))
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(main_blueprint)

    return app




