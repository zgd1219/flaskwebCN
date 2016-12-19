from . import auth
from flask import request, render_template, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm
from ..models import User
from .. import db
from ..email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.vefify_password(form.password.data):
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
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.passord.data)
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




