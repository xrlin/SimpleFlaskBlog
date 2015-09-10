# -*- coding : utf-8 -*-

from flask import Flask
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_migrate import Migrate
from . import config
bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = "auth.login"    # 设定未授权登录时跳转到的页面
pagedown = PageDown()   # 在线markdown编辑预览扩展
migrate = Migrate()

from .auth import auth as auth_blueprint
from .main import main as main_blueprint
from .admin import admin as admin_blueprint
from application.models import Article

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix="/admin")

    return app




