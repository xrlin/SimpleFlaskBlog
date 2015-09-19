from flask_wtf import Form
from wtforms import TextAreaField, SubmitField, StringField, HiddenField
from wtforms.validators import Required, DataRequired

__author__ = 'archer'


class CommentForm(Form):

    comment = TextAreaField("评论：", validators=[Required()])
    reply_to_id = HiddenField()
    reply_to_user = HiddenField()
    submit = SubmitField('提交')


class SearchForm(Form):

    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField('搜索')