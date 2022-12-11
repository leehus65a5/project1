from app import app, db
from app.model import Files, A10
from app.datamanager import datamanager
from app.form import UpLoadForm, DownloadForm
from flask import render_template, url_for, flash, redirect, g, request, send_file
from werkzeug.utils import secure_filename
import os
from io import BytesIO
from sqlalchemy import select

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
          flag = fileUp.upFile()
          if not flag:
               flash('Failse to upload file')
               return redirect(url_for('datamanager.uploadfile'))
          flash('upload file thành công')
     return render_template('datamanager/uploadfile.html', form=form)

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
     a10_data2 = A10.query.all()
     return render_template('datamanager/test.html', datas = a10_data2)