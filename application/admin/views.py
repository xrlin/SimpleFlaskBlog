#coding=utf-8
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from application import config
from flask import redirect, url_for, request, abort

'''
    权限控制
'''


class MicroBlogModelView(ModelView):

    def is_accessible(self):
        if not current_user.is_authenticated():
            return False
        elif not current_user.username == config.Admin:
            abort(403)
            return False
        return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))

''''

class CustomView(BaseView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated():
            return redirect(url_for('auth.login', next=request.url))
        elif not current_user.username == config.Admin:
            abort(403)
        return self.render('admin/index.html')
'''

'''
    后台管理博文界面
'''


class ArticleModelView(MicroBlogModelView):

    edit_template = 'admin/model/article-edit.html'
    create_template = 'admin/model/article-create.html'