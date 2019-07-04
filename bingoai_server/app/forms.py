from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class PictureForm(FlaskForm):
    picture = FileField(
        label=u'图片',
        validators=[DataRequired(u'上传图片不能为空')],
        render_kw={'accept': 'image/*', 'style': 'display:none', 'align': 'margin-top:10px'}
    )
    submit = SubmitField(
        u'提交',
        render_kw={'style': 'text-align: center; font-size:30px; margin-top:10px; margin-left:5px', 'align': 'center'}
    )
