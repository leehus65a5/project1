from app import db, mySql, app, User
from flask import render_template, url_for, flash, redirect, g
from app.admin import admin
from app.form import insert_form
from werkzeug.security import generate_password_hash
from sqlalchemy import select, or_

#Chỉ cho phép Admin có thể truy cập vào blueprint admin
@admin.before_request
def check_auth():
     if g.user:
          if not str(g.user.User.id).lower().startswith('ad'):
               return redirect(url_for('index'))

@admin.route('/dashboard')
def dashboard():
     return render_template('admin/dashboard.html')

@admin.route('/manage', methods=['GET','POST'])
def quan_ly_nhan_vien():
     form = insert_form()
     check = db.session.execute(select(User).where(or_(User.id == form.userid.data, User.email == form.email.data, User.username == form.username.data))).fetchone()
     users = db.session.execute(select(User)).fetchall()
     
     if form.validate_on_submit() and not check:
          passw = generate_password_hash(form.password.data)
          new_user = User(id=form.userid.data, email=form.email.data, username=form.username.data,password=passw)
          db.session.add(new_user)
          db.session.commit()
          flash('Đã thêm thành công 1 nhân viên')
     else:
          flash('có lỗi khi nhập dữ liệu')
     
     return render_template('admin/manage.html',form=form, users=users)

@admin.route('/update', methods=['GET', 'POST'])
def sua_nhan_vien():
     return render_template('admin/update.html')

#-------------CHECK ZONE CODE----------------------

@admin.route('/')
def test():
     x = check()
     return x

def check():
     #this is code how we can connect to the mysql databases
     cur = mySql.connection.cursor()
     cur.execute('select * from a10')
     rs = ''
     for i in range(20):
          rs += str(cur.fetchone()) + '<br>'
     
     rt = db.engine.execute('select * from users')
     rtt = ''
     for i in rt:
          rtt += str(i) + '<br>'
     
     a10 = db.Table('a10', db.metadata, autoload=True,autoload_with=db.engine)
     check33 = db.session.query(a10).all()
     cxx, k = '', 0
     for i in check33:
          cxx += str(i.DEPT) + '<br>'
          k += 1
          if k == 10:
               break
     
     # with app.app_context():
     #      Dean = Base.classes.dean
     #      cxx1 = db.session.query(Dean).all()
     #      x1 = ''
     #      for i in cxx1:
     #           x1 += str(i.DDIEM_DA) + '<br>'
     
     x1 = 'close'
     
     return f'<p> {rtt} </p> <h2> check </h2> <p> {x1} </p> <h2> check2 </h2> <p> {cxx} </p>'