from app import db, mySql
from flask import render_template, url_for, flash, redirect, g, request
from app.user import user
from app.model import A10

@user.route('/')
@user.route('/dashboard')
def dashboard():
     return render_template('user/dashboard.html')

@user.route('/test')
def showdata():
     a10_data2 = A10.query.all()
     x = a10_data2[0]
     print(x.__dict__.keys())
     return render_template('user/test.html', datas = a10_data2)