from app import db, app
from sqlalchemy import select

with app.app_context():
     db.reflect()

class User(db.Model):
     __table__ = db.metadata.tables['users']
     
     def creatUser(self):
          get_id = "".join(self.id)
          list_id = [str(i[0]).lower() for  i in db.session.execute(select(User.id)).fetchall()]
          if get_id in list_id:
               return 'User đã tồn tại trong database', False
          db.session.add(self)
          db.session.commit()
          return 'Tạo User thành công', True

     def updateUser(user_id, *args):
          get_id = "".join(user_id)
          get_user = User.query.filter_by(id = get_id).fetchone()
          if not get_user:
               return False
          pass
     
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
          return True
     
     def downloadFile(file_id):
          get_file = Files.query.filter_by(id = file_id).first()
          if not get_file:
               return False
          return get_file
          
     def __repr__(self) -> str:
          return f'File = ({self.id} : {self.filename})'

class A10(db.Model):
     __table__ = db.metadata.tables['a10']
     
     # def __repr__(self) -> str:
     #      return f'A10 = ({self.DEPT} : {self.PERM})'
     
     