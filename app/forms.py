from flask_wtf import FlaskForm  # 从flask_wtf包中导入FlaskForm类
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField  # 导入这些类
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    remember_me = BooleanField(_l('记住登录状态'))
    submit = SubmitField(_l('登录'))


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('当前用户名已被占用，请用一个新的用户名代替')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('当前邮箱已被占用，请用一个新的邮箱代替')




class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('重置密码')


class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    about_me = TextAreaField('关于我', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交')

    # 验证用户名
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('该用户名已被占用')


class PostForm(FlaskForm):
    post = TextAreaField('说些什么吧', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('提交')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('提交重置密码请求')