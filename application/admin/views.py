from flask import render_template, flash, request, current_app
from flask import Markup
from markdown import  markdown
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from application import config
from application.admin import admin
from application.admin.forms import PageDownForm
from application.models import Tag, Article
from application.models import Category

__author__ = 'archer'


@admin.route("/", methods=['POST', 'GET'])
@login_required
def index():
    if current_user.username != config.Admin:
        abort(403)
    form = PageDownForm()
    categories = [(name, name) for name in current_app.config['CATEGORIES']]
    form.category.choices = categories
    if request.method == 'POST' and form.validate():
        tags = []
        for name in form.tags.data.split(','):
            if Tag.query.filter_by(name=name).first():
                tags.append(Tag.query.filter_by(name=name).first())
            else:
                tags.append(Tag(name))
        name = form.category.data
        category_id = Category.query.filter_by(name=name).first().id
        context = Markup(markdown(form.pagedown.data))
        article = Article(form.title.data, context, None, 0, category_id, tags)
        article.save()
        flash("发表新文章成功")
    return render_template('admin/index.html', form=form, categories=categories)