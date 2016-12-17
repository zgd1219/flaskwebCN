from . import auth
from flask import request, render_template, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm
from ..models import User

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