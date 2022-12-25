from app import db, mySql, app, tools
from flask import render_template, url_for, flash, redirect, g, request, jsonify, session, send_file
from app.datamanager import datamanager
from app.model import A10, Udata, Files2, FileLog
from sqlalchemy import select, and_
from app.form import UpLoadForm, DownloadForm
from app import tools
from werkzeug.utils import secure_filename
import csv, os
from io import BytesIO
from sqlalchemy import select, and_


@datamanager.before_request
def check_auth():
     if g.user:
          check = str(g.user.User.id).lower()
          if check.startswith('u'):
               return redirect(url_for('index'))

@datamanager.route('/dashboard')
def dashboard():
     return render_template('datamanager/base.html')

@datamanager.route('/uploadfile', methods = ['GET', 'POST'])
def uploadfile():
     form = UpLoadForm()
     if form.validate_on_submit() and request.method == 'POST':
          file1 = form.fileup.data
          # file1 = request.files['fileup']
          file1_data = request.files['fileup'].read()
          file1.stream.seek(0)
          # file1.save(os.path.join(os.getcwd(), 'app' ,app.config['UPLOAD_FOLDER'],secure_filename(file1.filename)))
          file1.save(os.path.join(app.root_path, 'static', 'files', secure_filename(file1.filename)))
          fileUp = Files2(id = str(file1.filename.split('.')[0]), filename = file1.filename, data = file1_data)
          mess = fileUp.upFile()[1]          
          flash(mess)
          return redirect(url_for('datamanager.uploadfile'))
          
     return render_template('datamanager/uploadfile.html', form=form)

# @datamanager.route('/upload', methods = ['GET','POST'])
# def uploadfiles2():
     
#      form = UpLoadForm()
#      list_file_send = select(Files2.uploader,Files2.reviewer, Files2.wellid, Files2.status).where(Files2.uploader == g.user.User.id)
#      get_list_send = db.session.execute(list_file_send).fetchall()
     
#      list_hist = select(FileLog.uploader, FileLog.reviewer, FileLog.wellid, FileLog.status).where(FileLog.uploader == g.user.User.id)
#      get_list_hist = db.session.execute(list_hist).fetchall()
     
#      print(get_list_send, get_list_hist)
     
#      print('uid', g.user.User.id)
#      print('role', g.user.User.role)
     
#      print(request.form)
#      if form.validate_on_submit() and request.method == 'POST':
#           file1 = form.fileup.data
#           # file1 = request.files['fileup']
#           file1_data = request.files['fileup'].read()
#           file1.stream.seek(0)
#           # file1.save(os.path.join(os.getcwd(), 'app' ,app.config['UPLOAD_FOLDER'],secure_filename(file1.filename)))
#           path = os.path.join(app.root_path, 'static', 'files', secure_filename(file1.filename))
#           file1.save(path)
#           print('path = ' , path)
#           curinfo, wellinfo, df = tools.convert_lasio(path)
#           fileUp = Files2(
#                uploader = g.user.User.id,
#                reviewer = g.user.User.ngquanly,
#                wellid = file1.filename.split('.')[0],
#                cur_info = curinfo,
#                well_info = wellinfo,
#                data = df.to_json(),
#                status = 'pending',
#           )
#           db.session.add(fileUp)
#           db.session.commit()         
#           print('ok here')
#           return redirect(url_for('datamanager.uploadfiles2'))
          
#      return render_template('datamanager/upload.html', form=form, sendfiles = get_list_send, hist = get_list_hist) 

@datamanager.route('/recive', methods=['GET', 'POST'])
def manage_recivefile():
     
     list_recive_file = select(Files2.uploader,Files2.reviewer, Files2.wellid, Files2.status).where(and_(Files2.reviewer == g.user.User.id, Files2.status == 'pending'))
     get_list_recive = db.session.execute(list_recive_file).fetchall()
     
     return render_template('datamanager/recive.html', recives = get_list_recive)

@datamanager.route('/download', methods=['GET', 'POST'])
def downloadfile():
     form = DownloadForm()
     if form.validate_on_submit() and request.method == 'POST':
          file_id = form.file_id.data
          get_file = Files.downloadFile(file_id)
          if not get_file:
               flash('no file to download')
               return redirect(url_for('datamanager.downloadfile'))
          flash('download file thành công')
          return send_file(BytesIO(get_file.data),download_name=get_file.filename,as_attachment=True)
     return render_template('datamanager/downloadfile.html', form=form)

@datamanager.route('/test', methods = ['GET','POST'])
def test():
     return render_template('datamanager/test.html')

@datamanager.route('/plot')
def plot():
     return render_template('datamanager/plotdata.html')


@datamanager.route('/check', methods=['GET', 'POST'])
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
          return render_template('datamanager/data.html', datas = None, listkey = None)
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
     return render_template('datamanager/data.html', datas = data, listkey = listk, listTable = listTable)