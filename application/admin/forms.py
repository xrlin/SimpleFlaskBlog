from flask import current_app
from flask_wtf import Form
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField, StringField, SelectField
from wtforms.validators import Required


class PageDownForm(Form):

    title = StringField("Title", validators=[Required()])
    category = SelectField("Category", validators=[Required()])
    tags = StringField("Tags", validators=[Required()])
    pagedown = PageDownField('Edit Article', validators=[Required()])
    submit = SubmitField('Submit')
