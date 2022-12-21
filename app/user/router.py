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
    print('this is listTable', listTable)
    listTable = [i.tableid for i in listTable]
    print(listTable)
    print('uid', uid)

    if request.method == 'POST':
        form = request.form
        if 'all' not in form:
            cols = [i for i in form if i not in ['start', 'stop', 'all', 'save']]
            sql = select(A10.DEPT, *[getattr(A10, i) for i in cols]).where(
                and_(A10.DEPT >= form['start'], A10.DEPT <= form['stop']))
            r = db.session.execute(sql).fetchall()
            a10_data2 = r

        return render_template('user/test.html', datas=a10_data2, listkey=listkey, listTable=listTable)

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

    return render_template('user/test.html', datas=a10_data2, listkey=listkey, listTable=listTable)


@user.route('/check', methods=['GET', 'POST'])
def check():
    data = None
    listk = None
    form = request.form
    check_table = session.get('table')

    if not check_table:
        print('not check table')
        if 'name' in form:
            print('name in form')
            session['table'] = form['name']

    if check_table:
        print('đã có table')
        if 'name' in form:
            if len(form['name']) >= 1 and form['name'] != check_table:
                session['table'] = form['name']

    if request.method == 'POST':
        pass
        print('check form', form)
        data = db.session.execute(select(cls)).fetchall()

    # a10 = db.Table('a10', db.metadata,autoload=True,autoload_with=db.engine)
    # sql = select(a10)
    # r = db.session.execute(sql).fetchall()
    # for i in r:
    #      print(i)

    return render_template('user/check.html', datas=data, listkey=listk)
