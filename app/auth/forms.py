from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email
from wtforms import StringField, SubmitField, BooleanField, PasswordField

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'),
                                          Length(1,64),Email(message='请输入正确的邮箱格式！')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空！')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')
