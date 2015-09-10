from flask_wtf import Form
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import Required, DataRequired

__author__ = 'archer'


class CommentForm(Form):

    comment = TextAreaField("评论：", validators=[Required()])
    submit = SubmitField('提交')


class SearchForm(Form):

    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField('搜索')