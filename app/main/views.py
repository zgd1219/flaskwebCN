from . import main
from flask import request, render_template, abort, flash, url_for,redirect, current_app
from flask_login import current_user, login_required
from ..models import User, Role, Post, Permission
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from .. import db
from ..decorators import admin_required,permission_required

@main.route('/', methods=["GET", "POST"])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
                page=page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, form=form, pagination=pagination)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
                page=page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False )
    posts = pagination.items
    return render_template("user.html", user=user, posts=posts, pagination=pagination)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("资料编辑保存成功")
        return redirect(url_for("main.user", username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", form=form)

@main.route('/edit-profile/<int:id>', methods=["GET", "POST"])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        user.username = form.username.data
        user.email = form.email.data
        user.role = Role.query.get(form.role.data)
        user.confirmed = form.confirmed.data
        db.session.add(user)
        flash("资料编辑保存成功!")
        return redirect(url_for("main.user", username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template("edit_profile.html", form=form, user=user)

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
        not current_user.is_administrator():
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body=form.body.data
        db.session.add(post)
        flash("文章编辑成功!")
        return redirect(url_for("main.post", id=post.id))
    form.body.data=post.body
    return render_template("edit_post.html", form=form)

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("用户不存在!")
        return redirect(url_for(".index"))
    if current_user.is_following(user):
        flash("已经关注了该用户!")
        return redirect(url_for(".user", username=user.username))
    current_user.follow(user)
    flash("你成功关注了%s!" %user.username)
    return redirect(url_for(".user", username=username))

@main.route("/follow/<username>")
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("该用户不存在!")
        return redirect(url_for(".index"))
    if not current_user.is_following(user):
        flash("你没有关注此用户!")
        return redirect(url_for(".user", username=username))
    current_user.unfollow(user)
    flash("你取消了对%s的关注!" %username)
    return redirect(url_for(".user", username=username))

@main.route("/followers/<username>")
def followers(username):
    return render_template("followers.html")

@main.route("/followed-by/<username>")
def followed_by(username):
    return render_template("followers.html")