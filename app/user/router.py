from app import db, mySql
from flask import render_template, url_for, flash, redirect, g, request
from app.user import user
from app.model import A10
from app.form import GetInfoForm
from sqlalchemy import select, and_

@user.route('/')
@user.route('/dashboard')
def dashboard():
     return render_template('user/dashboard.html')

@user.route('/test', methods = ['GET','POST'])
def showdata():
     a10_data2 = A10.query.all()
     x = a10_data2[0]
     listkey = x.__dict__.keys()
     listkey = sorted(listkey)[1:-1]
     
     if request.method == 'POST':
          form = request.form
          cols = [i for i in form if i not in ['start', 'stop']]
          sql = select(A10.DEPT,*[getattr(A10, i) for i in cols]).where(and_(A10.DEPT >= form['start'], A10.DEPT <= form['stop']))
          r = db.session.execute(sql).fetchall()
          a10_data2 = r
          
     return render_template('user/test.html', datas = a10_data2, listkey = listkey)