from flask import Flask
from app.config import Config
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

app = Flask(__name__)
app.config.from_object(Config)
mySql = MySQL(app)
db = SQLAlchemy(app)

with app.app_context():
     db.reflect()

class User(db.Model):
     __table__ = db.metadata.tables['users']
     
     def creatUser(self):
          get_id = "".join(self.id)
          list_id = [i[0] for  i in db.session.execute(select(User.id)).fetchall()]
          if get_id in list_id:
               return False
          db.session.add(self)
          db.session.commit()
          return True
     
     def __repr__(self):
        return f'User({self.id} : {self.username})'

class Files(db.Model):
     __table__ = db.metadata.tables['files']
     
     def upFile(self):
          get_id = "".join(self.id)
          list_id = [i[0] for i in db.session.execute(select(Files.id)).fetchall()]
          if get_id in list_id:
               return False
          db.session.add(self)
          db.session.commit()
     
     def downloadFile(file_id):
          get_file = Files.query.filter_by(id = file_id).first()
          if not get_file:
               return False
          return get_file
          
     def __repr__(self) -> str:
          return f'File = ({self.id} : {self.filename})'
     
     
from app.admin import admin 
app.register_blueprint(admin)

from app.datamanager import datamanager
app.register_blueprint(datamanager)

from app.user import user
app.register_blueprint(user, url_prefix = '/user')

from app import main

# with app.app_context():
# 	BaseSql = automap_base()
# 	BaseSql.prepare(db.engine, reflect = True)
# 	User = BaseSql.classes.users 
	# User = db.Table('users',db.metadata,autoload=True,autoload_with=db.engine)


     # for i in db.metadata.tables:
     #      print('table = ', i)
# User = db.metadata.tables['users']