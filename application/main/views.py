from . import main
from flask import session, render_template, current_app, request, flash
from flask_login import current_user, login_required
from werkzeug.utils import redirect
from application.main.forms import CommentForm, SearchForm
from application.models import Article, Tag, Category, Comment

__author__ = 'archer'


@main.route("/")
@main.route("/<int:page>")
def index(page=1):
    tags = Tag.query.all()
    categories = Category.query.all()
    pagination = Article.query.paginate(page, per_page=current_app.config['PER_PAGE'])
    return render_template("index.html", categories=categories, tags=tags, pagination=pagination)


@main.route("/user/<username>")
@login_required
def user(username):
    if not username == current_user.username:
        return redirect("auth.login")
    return render_template("user.html", username=username)


@main.route("/category/<int:id>")
def category(id):
    tags = Tag.query.all()
    categories = Category.query.all()
    articles = Category.query.get(id).articles
    try:
        page = int(request.args.get('page'))
    except:
        page = 1
    pagination = articles.paginate(page=page, per_page=current_app.config['PER_PAGE'])
    return render_template("category_query.html", categories=categories, tags=tags, pagination=pagination)


@main.route("/tag/<int:id>")
def tag(id):
    tags = Tag.query.all()
    categories = Category.query.all()
    this_tag = Tag.query.get(id)
    articles = Article.query.filter(Article.tags.contains(this_tag))    # 存放包含该tag的article的query对象
    try:
        page = int(request.args.get('page'))
    except:
        page = 1
    pagination = articles.paginate(page=page, per_page=current_app.config['PER_PAGE'])
    return render_template("tag_query.html", categories=categories, tags=tags, pagination=pagination)


@main.route("/article/<int:id>", methods=['POST', 'GET'])
def article(id):
    form = CommentForm()
    tags = Tag.query.all()
    categories = Category.query.all()
    article = Article.query.get(id)
    article.view_count += 1
    article.save()
    parent_comments = [c for c in article.comments if not c.parent_id]  # 获取该文章的所有最顶级（parent)评论
    if form.validate_on_submit():
        comment_body = form.comment.data
        parent_id = request.args.get('replytoid') or None
        comment = Comment(user_id=current_user.id, body=comment_body, article_id=id, parent_id=parent_id)
        comment.save()
        flash("成功提交评论")
        if not parent_id:
            parent_comments.append(comment)
    return render_template("article.html", categories=categories, tags=tags,
                           article=article, form=form, Comment=Comment, parent_comments=parent_comments)


@main.route("/search", methods=['POST', 'GET'])
def search():
    categories = Category.query.all()
    tags = Tag.query.all()
    try:
        page = int(request.args.get('page'))
    except:
        page = 1
    if request.args.get('search'):
        search_text = request.args.get('search')
        session['search'] = search_text  # 用session暂存数据为了分页准备
    else:
        search_text = session.get('search')
    pagination = Article.query.search(search_text).\
        paginate(page=page, per_page=current_app.config['PER_PAGE'])
    for i in pagination.items:
        print(i)
    return render_template("search_result.html", categories=categories, tags=tags, pagination=pagination)


