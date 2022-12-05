from flask import Flask
from app.config import Config
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.config.from_object(Config)
mySql = MySQL(app)
db = SQLAlchemy(app)

with app.app_context():
     db.reflect()

class User(db.Model):
     __table__ = db.metadata.tables['users']
     def __repr__(self):
        return f'User({self.id} : {self.username})'
     
from app.admin import admin 
app.register_blueprint(admin, url_prefix='/admin',template_folder = 'templates/admin')

from app.user import user
app.register_blueprint(user, url_prefix = '/user')

from app.datamanager import datamanager
app.register_blueprint(datamanager, url_prefix = '/datamanager')

from app import main

# with app.app_context():
# 	BaseSql = automap_base()
# 	BaseSql.prepare(db.engine, reflect = True)
# 	User = BaseSql.classes.users 
	# User = db.Table('users',db.metadata,autoload=True,autoload_with=db.engine)


     # for i in db.metadata.tables:
     #      print('table = ', i)
# User = db.metadata.tables['users']