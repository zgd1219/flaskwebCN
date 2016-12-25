from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'),
                                          Length(1,64),Email(message='请输入正确的邮箱格式！')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空！')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(),
                                          Length(1,64), Email(message='请输入正确的邮箱格式!')])
    username = StringField('昵称', validators=[DataRequired(),
                                             Length(1,20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1,20),
                                              EqualTo('password2', message="两次密码不匹配!")])
    password2 = PasswordField('确认密码', validators=[DataRequired(),Length(1,20)])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("该邮箱已经被注册！")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[DataRequired()])
    passowrd = PasswordField('新密码', validators=[DataRequired(), Length(1,20),
                                                EqualTo('password2', message='两次密码不一致！')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('提交')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(),
                        Length(1,64), Email(message='请输入正确的邮箱格式！')])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError("该邮箱未注册!请输入正确的邮箱地址")

class PasswordRestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(),
                        Length(1,64), Email(message='请输入正确的邮箱格式！')])
    passowrd = PasswordField('新密码', validators=[DataRequired(), Length(1,20),
                                                EqualTo('password2', message='两次密码不一致！')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError("该邮箱未注册!请输入正确的邮箱地址")

class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱', validators=[DataRequired(),
                        Length(1, 64), Email(message='请输入正确的邮箱格式！')])
    password = PasswordField('密码', validators=[DataRequired(),Length(1,20)])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册.')


