from app import db, mySql, app
from flask import render_template, url_for, flash, redirect, g, request, jsonify, session
from app.user import user
from app.model import A10, Udata
from sqlalchemy import select, and_
import csv, os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import mapper


@user.route('/')
@user.route('/dashboard')
def dashboard():
    return render_template('user/dashboard.html')


@user.route('/test', methods=['GET', 'POST'])
def showdata():
     a10_data2 = A10.query.all()
     x = a10_data2[0]
     listkey = x.__dict__.keys()
     listkey = sorted(listkey)[1:-1]
     # d = []
     
     uid = session.get('user_id')
     listTable = db.session.execute(select(Udata.tableid).where(Udata.userid == uid))
     listTable = [i.tableid for i in listTable]
     
     if request.method == 'POST':
          form = request.form
          if 'all' not in form:
               cols = [i for i in form if i not in ['start', 'stop','all','save']]
               sql = select(A10.DEPT,*[getattr(A10, i) for i in cols]).where(and_(A10.DEPT >= form['start'], A10.DEPT <= form['stop']))
               r = db.session.execute(sql).fetchall()
               a10_data2 = r
               
          return render_template('user/test.html', datas = a10_data2, listkey = listkey, listTable = listTable)
     
     # for i in a10_data2:
     #      d.append(i.to_dict())
          
     # path1 = os.path.join(app.root_path, 'user/static/files/', 'saveFiles.csv')
     # print(path1)
     # with open(path1, 'w', newline='') as f:
     #      dict_writer = csv.DictWriter(f, d[0].keys())
     #      dict_writer.writeheader()
     #      dict_writer.writerows(d)
     
     print(type(a10_data2[0]))
     print(a10_data2[0])
     print(a10_data2[0].__dict__)
     print(sorted(a10_data2[0].__dict__))
     
     return render_template('user/test.html', datas = a10_data2, listkey = listkey, listTable = listTable)




@user.route('/check', methods=['GET', 'POST'])
def check():
     uid = session.get('user_id')
     listTable = db.session.execute(select(Udata.tableid).where(Udata.userid == uid))
     listTable = [i.tableid for i in listTable]
     
     data = None
     listk = None
     form = request.form
     check_table = session.get('table')
     
     print('check table', check_table)
     
     if 'name' not in form and not check_table:
          print('no name and check table')
          return render_template('user/check.html', datas = None, listkey = None)
     print('here')
     
     
     if request.method == 'POST':
          if 'name' in form and len(form['name']) >= 1:
               session['table'] = form['name']
               tb_cls = db.Table(session['table'], db.metadata,autoload=True,autoload_with=db.engine)
               data = db.session.execute(select(tb_cls)).fetchall()
               listk = [i.name for i in tb_cls.columns]
               listk = sorted(listk)
               print('check1')
               print(session['table'])
               # return render_template('user/check.html', datas = data, listkey = listk)
          elif 'start' in form:
               print('check 2 name not in table, get selected collums')
               print(form)
               listk = [i for i in form if i not in ['start', 'stop']]
               print(listk)
               tb_cls = db.Table(session['table'], db.metadata,autoload=True,autoload_with=db.engine)
               sql = select(*[getattr(tb_cls.c, i) for i in listk]).where(and_(tb_cls.c.DEPT >= form['start'], tb_cls.c.DEPT <= form['stop']))
               data = db.session.execute(sql).fetchall()
               print('check2')
               # return render_template('user/check.html', datas = data, listkey = listk)
          else:
               tb_cls = db.Table(session['table'], db.metadata,autoload=True,autoload_with=db.engine)
               data = db.session.execute(select(tb_cls)).fetchall()
               listk = [i.name for i in tb_cls.columns]
               listk = sorted(listk)
               print(listk)
               print('check3')
               # return render_template('user/check.html', datas = data, listkey = listk)
          
          print('check4')
          
     # a10 = db.Table('a10', db.metadata,autoload=True,autoload_with=db.engine)
     # sql = select(a10)
     # r = db.session.execute(sql).fetchall()
     # for i in r:
     #      print(i)
     
     print('chech5')
     return render_template('user/check.html', datas = data, listkey = listk, listTable = listTable)
