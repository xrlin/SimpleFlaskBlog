from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Length, Email, EqualTo
from wtforms.validators import Required
from ..models import User

__author__ = 'archer'
# -*- coding : utf-8 -*-


class LoginForm(Form):

    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('保持等录')
    submit = SubmitField('登录')


class RegisterForm(Form):

    username = StringField('Username', validators=[Required()])
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators= \
        [Required(), EqualTo('confirm_password', message='两次输入的密码必须相同')])
    confirm_password = PasswordField('Retype Password', validators=[Required()] )
    submit = SubmitField("注册")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该Email已经注册过了，请重新输入')

    def validate_username(self, field):
        if User.query.get_user_by_name(field.data):
            raise ValidationError('该用户名已经注册过了，请重新输入')


class ChangePasswordForm(Form):

    old_password = PasswordField('请确认旧密码：', validators=[Required()])
    password = PasswordField('请输入新密码：', validators= \
        [Required(), EqualTo('confirm_password', message='两次输入的密码必须相同')])
    confirm_password = PasswordField('重新输入新密码：', validators=[Required()])
    submit = SubmitField('确认更改')


class ResetPasswordRequestForm(Form):

    email = StringField('请输入验证邮箱', validators=[Required(), Email()])
    submit = SubmitField('发送验证连接')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('该邮箱未注册，请输入正确的邮箱')


class ResetPasswordForm(Form):

    email = StringField('请输入验证邮箱', validators=[Required(), Email()])  # 该email用来确认用户
    password = PasswordField('请输入新密码：', validators= \
        [Required(), EqualTo('confirm_password', message='两次输入的密码必须相同')])
    confirm_password = PasswordField('重新输入新密码：', validators=[Required()])
    submit = SubmitField('确认更改')

    # 校验是否是已注册邮箱
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('该邮箱未注册，请输入正确的邮箱')

class ChangeEmailForm(Form):

    email = StringField('请输入新邮箱：', validators=[Required(), Email()])
    submit = SubmitField('提交更改申请')

    # 校验是否是已注册邮箱
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该Email已经注册过了，请重新输入')