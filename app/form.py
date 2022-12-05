from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class loginForm(FlaskForm):
     username = StringField("Tên đăng nhập",validators=[DataRequired()])
     password = PasswordField("Mật khẩu", validators=[DataRequired()])
     remember = BooleanField("Ghi nhớ")
     submit = SubmitField("Đăng nhập")

class insert_form(FlaskForm):
     username = StringField("Tên Nhân Viên")
     userid = StringField("id", validators=[DataRequired()])
     email = StringField("email",validators=[DataRequired()])
     password = PasswordField('Mật khẩu', validators=[DataRequired()])
     submit = SubmitField("Thêm nhân viên")