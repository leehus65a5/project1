from app import db, mySql, app
from flask import render_template, url_for, flash, redirect, g, request, jsonify
from app.user import user
from app.model import A10
from sqlalchemy import select, and_
import csv, os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import mapper


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
     # d = []
     
     if request.method == 'POST':
          form = request.form
          if 'all' not in form:
               cols = [i for i in form if i not in ['start', 'stop','all','save']]
               sql = select(A10.DEPT,*[getattr(A10, i) for i in cols]).where(and_(A10.DEPT >= form['start'], A10.DEPT <= form['stop']))
               r = db.session.execute(sql).fetchall()
               a10_data2 = r
               
          # return render_template('user/test.html', datas = a10_data2, listkey = listkey)
     
     # for i in a10_data2:
     #      d.append(i.to_dict())
          
     # path1 = os.path.join(app.root_path, 'user/static/files/', 'saveFiles.csv')
     # print(path1)
     # with open(path1, 'w', newline='') as f:
     #      dict_writer = csv.DictWriter(f, d[0].keys())
     #      dict_writer.writeheader()
     #      dict_writer.writerows(d)
                    
     return render_template('user/test.html', datas = a10_data2, listkey = listkey)


@user.route('/check')
def check():
     a10 = db.Table('a10', db.metadata,autoload=True,autoload_with=db.engine)
     
     sql = select(getattr(a10.columns, 'DEPT'), getattr(a10.columns, 'PERM'))
     r = db.session.execute(sql).fetchall()
     for i in r:
          print(i)
     return render_template('user/check.html', datas = 'ac')
