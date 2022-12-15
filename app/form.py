from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired


class LoginForm(FlaskForm):
     username = StringField("Tên đăng nhập",validators=[DataRequired()])
     password = PasswordField("Mật khẩu", validators=[DataRequired()])
     remember = BooleanField("Ghi nhớ")
     submit = SubmitField("Đăng nhập")

class InsertForm(FlaskForm):
     username = StringField("Tên Nhân Viên", validators=[DataRequired()])
     userid = StringField("id", validators=[DataRequired()])
     email = StringField("email",validators=[DataRequired()])
     password = PasswordField('Mật khẩu', validators=[DataRequired()])
     submit = SubmitField("Thêm nhân viên")
     
class UpdateForm(FlaskForm):
     id = StringField("id", validators=[DataRequired()])
     username = StringField("Tên Nhân Viên")
     email = StringField("email")
     password = PasswordField('Mật khẩu')
     submit = SubmitField("Update nhân viên")

class UpLoadForm(FlaskForm):
     fileup = FileField('Chọn file bạn muốn tải lên', validators=[FileRequired()])
     submit_upload = SubmitField('Upload file')
      
class DownloadForm(FlaskForm):
     file_id = StringField('Nhập tên file', validators=[DataRequired()])
     submit_download = SubmitField('Donwload file')
