from . import auth
from flask import request, render_template, redirect, flash, url_for,current_app
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, \
    PasswordRestForm, ChangeEmailForm
from ..models import User
from .. import db
from ..email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("登录成功！")
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("用户名或密码错误！")
    return render_template('auth/login.html', form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("用户已退出！")
    return redirect(url_for("auth.login"))

@auth.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(current_app.config['FLASKY_ADMIN'])
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, "账号确认",'auth/email/confirm',
                   user=user, token=token)
        flash("已经发送确认信到您的邮箱，请及时确认!")
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    elif current_user.confirm(token):
        flash('账号激活成功!')
    else:
        flash('确认链接已经失效或过期！')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.':
            flash("请先确认你的账号！")
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.confirmed or current_user.is_anonymous:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,"账号确认",
               "auth/email/confirm", token=token, user=current_user)
    flash("一封信的确认信已经发送到你的邮箱!")
    return redirect(url_for('main.index'))

@auth.route('/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.passowrd.data
            db.session.add(current_user)
            flash("密码修改成功!")
            return redirect(url_for("main.index"))
        flash("请输入正确的原始密码!")
    return render_template("auth/change_password.html", form=form)

@auth.route("/password_reset_request", methods=["GET", "POST"])
def password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, "重置密码", "auth/email/reset_password",
                       token=token, user = user)
            flash("重置密码邮件已发送到您的邮箱，请查收!")
            return redirect(url_for('auth.login'))
        flash("请输入正确的邮箱地址!")
    return render_template('auth/reset_password.html', form=form)

@auth.route('/password_reset/<token>', methods=['POST', 'GET'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = PasswordRestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("请输入正确的邮件地址!")
            return redirect(url_for('auth.login'))
        if user.reset_password(token, form.passowrd.data):
            flash("密码重置成功")
            return redirect(url_for('auth.login'))
        else:
            flash("请输入正确的邮件地址!")
            return redirect(url_for('auth.password_reset', token=token))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=["GET", "POST"])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, "更换邮箱", "auth/email/change_email",
                       token=token, user=current_user)
            flash("邮箱更换确认信已经发送到新邮箱!")
            return redirect(url_for('main.index'))
        else:
            flash("请输入正确的密码!")
    return render_template("auth/change_email.html", form=form)

@auth.route('/change_email/<token>', methods=['POST', 'GET'])
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash("邮箱更改成功!新的邮箱地址为" + current_user.email)
    else:
        flash("邮箱更改失败")
    return redirect(url_for("main.index"))







