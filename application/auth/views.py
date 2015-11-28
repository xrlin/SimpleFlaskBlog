#coding=utf-8
from . import auth
from flask_login import login_user, login_required, current_user, logout_user
from application.utils.mail import send_mail
from .forms import RegisterForm, LoginForm, ChangeEmailForm, ChangePasswordForm, ResetPasswordForm, \
    ResetPasswordRequestForm
from ..models import User
from flask import flash, url_for, redirect, render_template, request
from application import config

__author__ = 'archer'


@auth.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.get_user_by_name(form.username.data)
        if u and u.verify_password(form.password.data):
            login_user(u, remember=form.remember_me.data)
            # flash("成功登录，即将跳转回首页")
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("用户名或密码不正确")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    # flash("you have log out")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(form.username.data, form.email.data, form.password.data)
        u.save()
        token = u.generate_confirmation_token()
        token_url = config.token_url_template.format(str(token, 'utf-8'))
        send_mail(subject=config.SUBJECT_HEADER, recipients=[u.email], token_url=token_url)
        flash('注册成功，稍后请点击发送到注册邮箱的连接完成验证')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route("/confirm/<token>", methods=['POST', 'GET'])
@login_required
def confirm(token):
    u = current_user
    if u.confirmed:
        flash("您的帐号已经验证过了，不需再次验证")
        return redirect(url_for("main.index"))
    if not u.confirm(token):
        flash("该验证信息不符合或者已经过期，可以重新发送信息进行验证")
        return render_template("auth/unconfirm.html")
    flash("验证成功")
    u.confirm = True
    u.save()
    return redirect(url_for("main.index"))


@auth.route("/resend", methods=['POST', 'GET'])
@login_required
def resend():
    u = current_user
    token = u.generate_confirmation_token()
    token_url = config.token_url_template.format(str(token, 'utf-8'))
    send_mail(subject=config.SUBJECT_HEADER, recipients=[u.email], token_url=token_url)
    flash("验证信息已经重新发送至您的邮箱，请注意查收")
    return render_template("auth/unconfirm.html")


@auth.route("/change-password", methods=['POST', 'GET'])
@login_required
def change_password():
    form = ChangePasswordForm()
    u = current_user
    if form.validate_on_submit():
        if u.verify_password(form.old_password.data):
            flash("密码验证错误，请重新输入")
        u.password = form.password.data
        u.save()
        flash("成功更改密码")
        return redirect(url_for('.login'))
    return render_template("auth/change-password.html", form=form)


@auth.route("/change-email-request", methods=['POST', 'GET'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    u = current_user
    if form.validate_on_submit():
        new_email = form.email.data
        token = u.generate_change_email_token(new_email)
        token_url = config.token_url_template.format(str(token, 'utf-8'))
        send_mail(subject=config.SUBJECT_HEADER, recipients=[new_email], token_url=token_url)
        return "邮箱验证连接已经发送到您的邮箱，请注意查收"
    return render_template('auth/change-email-request.html', form=form)


@auth.route("/reset-password-request", methods=['POST', 'GET'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u is not None:
            token = u.generate_reset_token()
            token_url = config.token_url_template.format(str(token, 'utf-8'))
            send_mail(subject=config.SUBJECT_HEADER, recipients=[u.email], token_url=token_url)
            flash("密码重置验证连接已经发送到您的邮箱，请注意查收")
    return render_template("auth/reset-password.html", form=form)


@auth.route("/reset-password/<token>", methods=['POST', 'GET'])
def reset_password(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u.confirm_reset_token(token):
            u.password = form.password.data
            u.save()
            flash('成功重置密码')
    else:
        flash("重置密码失败，请确认验证邮箱和验证链接是否有误")
    return render_template("auth/reset-password.html", form=form)


@auth.route("/confirm-change-email/<token>")
@login_required
def confirm_change_email(token):
    u = current_user
    if u.change_email(token):
        return "成功更改并验证邮箱<a href=\"{0}\">返回首页</a>".format(url_for('main.index'))
    return "该验证信息不符合或者已经过期，可以重新发送信息进行验证"