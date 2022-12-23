from app import app, db
from app.model import Files, A10, Files2
from app.datamanager import datamanager
from app.form import UpLoadForm, DownloadForm
from flask import render_template, url_for, flash, redirect, g, request, send_file
from werkzeug.utils import secure_filename
import os
from io import BytesIO
from sqlalchemy import select
from app import tools
from datetime import datetime

@datamanager.before_request
def check_auth():
     if g.user:
          check = str(g.user.User.id).lower()
          if check.startswith('u'):
               return redirect(url_for('index'))

@datamanager.route('/dashboard')
def dashboard():
     return render_template('datamanager/dashboard.html')

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
          fileUp = Files(id = str(file1.filename.split('.')[0]), filename = file1.filename, data = file1_data)
          mess = fileUp.upFile()[1]          
          flash(mess)
          return redirect(url_for('datamanager.uploadfile'))
          
     return render_template('datamanager/uploadfile.html', form=form)

@datamanager.route('/upload', methods = ['GET','POST'])
def uploadfiles2():
     
     form = UpLoadForm()
     list_files_manager = select(Files2.userid, Files2.wellid, Files2.status).where(Files2.userid == g.user.User.id)
     get_list_file = db.session.execute(list_files_manager).fetchall()
     print(get_list_file)
     print('uid', g.user.User.id)
     
     print(request.form)
     if form.validate_on_submit() and request.method == 'POST':
          file1 = form.fileup.data
          # file1 = request.files['fileup']
          file1_data = request.files['fileup'].read()
          file1.stream.seek(0)
          # file1.save(os.path.join(os.getcwd(), 'app' ,app.config['UPLOAD_FOLDER'],secure_filename(file1.filename)))
          path = os.path.join(app.root_path, 'static', 'files', secure_filename(file1.filename))
          file1.save(path)
          print('path = ' , path)
          curinfo, wellinfo, df = tools.convert_lasio(path)
          fileUp = Files2(
               userid = g.user.User.id,
               wellid = file1.filename.split('.')[0],
               cur_info = curinfo,
               well_info = wellinfo,
               data = path,
               status = 'pending',
          )
          db.session.add(fileUp)
          db.session.commit()         
          print('ok here')
          return redirect(url_for('datamanager.uploadfiles2'))
          
     return render_template('datamanager/upload.html', form=form, listf = get_list_file)

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