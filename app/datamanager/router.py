from app import db, mySql, app, tools
from flask import render_template, url_for, flash, redirect, g, request, jsonify, session, send_file
from app.datamanager import datamanager
from app.model import A10, Udata, Files2, FileLog, Files
from sqlalchemy import select, and_, update
from app.form import UpLoadForm, DownloadForm
from app import tools
from werkzeug.utils import secure_filename
import csv, os
import pandas as pd
from io import BytesIO


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


@datamanager.route('/recive', methods=['GET', 'POST'])
def manage_recivefile():
     
     list_recive_file = select(Files2.uploader,Files2.reviewer, Files2.wellid, Files2.status).where(and_(Files2.reviewer == g.user.User.id, Files2.status == 'pending'))
     get_list_recive = db.session.execute(list_recive_file).fetchall()
     
     print(request.form)
     
     if request.method == 'POST':
          get_form = request.form
          uploader = get_form['upload']
          wellid = get_form['wellid']
          get_file = select(Files2.reviewer, Files2.cur_info, Files2.well_info, Files2.data).where(
          and_(Files2.uploader == uploader, Files2.wellid == wellid))
          files = db.session.execute(get_file).fetchone()
          
          if 'choose' in get_form and get_form['choose'] == 'reject':
               print('reject')
               check = Files2.update(uploader=uploader, 
                                     reviewer=files.reviewer, 
                                     wellid=wellid, 
                                     cur_info=files.cur_info, 
                                     wellinfo= files.well_info,
                                     status='reject')
               if check:
                    flash('reject sucssesfull')
               return redirect(url_for('datamanager.manage_recivefile'))

          if 'choose' in get_form and get_form['choose'] == 'accept':
               print('accpept')
               if g.user.User.role in ['admin','data']:
                    well_data_df = pd.read_json(files.data)
                    print(well_data_df)
                    try:
                         well_data_df.to_sql(con=db.engine, name=str.lower(wellid), if_exists='replace')
                         check = Files2.update(uploader=uploader, 
                                     reviewer=files.reviewer, 
                                     wellid=wellid, 
                                     cur_info=files.cur_info, 
                                     wellinfo= files.well_info,
                                     status='accept')
                         flash('to database successfull')
                         return redirect(url_for('datamanager.manage_recivefile'))
                    except:
                         flash('error while update file to database')
                         return redirect(url_for('datamanager.manage_recivefile'))
               else:
                    reciver_id = g.user.User.ngquanly
                    sql = update(Files2).where(and_(Files2.uploader == uploader, Files2.wellid == wellid)).values(reviewer=reciver_id)
                    db.session.execute(sql)
                    db.session.commit()
                    flash('updated')
                    return redirect(url_for('datamanager.manage_recivefile'))
          
          if 'choose' in get_form and get_form['choose'] == 'review':
               cur = files.cur_info
               well = files.well_info
               df = pd.read_json(files.data)
               df = df.to_html()
               # return redirect(url_for('user.preview'))
               return render_template('user/preview.html', df = df)
     
     return render_template('datamanager/recive.html', recives = get_list_recive)

@datamanager.route('/download', methods=['GET', 'POST'])
def downloadfile():
     msg = ""
     form = DownloadForm()
     if form.validate_on_submit() and request.method == 'POST':
          file_id = form.file_id.data
          get_file = Files.downloadFile(file_id)
          if not get_file:
               flash('no file to download')
               return redirect(url_for('datamanager.downloadfile'))
          msg = 'download file thành công'
          return send_file(BytesIO(get_file.data),download_name=get_file.filename,as_attachment=True)
     return render_template('datamanager/downloadfile.html', form=form, msg = msg)

@datamanager.route('/test', methods = ['GET','POST'])
def test():
     return render_template('datamanager/test.html')


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