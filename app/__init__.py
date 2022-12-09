from flask import Flask
from app.config import Config
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
mySql = MySQL(app)
db = SQLAlchemy(app)
     
from app.admin import admin 
app.register_blueprint(admin)

from app.datamanager import datamanager
app.register_blueprint(datamanager)

from app.user import user
app.register_blueprint(user)

from app import main

# with app.app_context():
# 	BaseSql = automap_base()
# 	BaseSql.prepare(db.engine, reflect = True)
# 	User = BaseSql.classes.users 
	# User = db.Table('users',db.metadata,autoload=True,autoload_with=db.engine)


     # for i in db.metadata.tables:
     #      print('table = ', i)
# User = db.metadata.tables['users']