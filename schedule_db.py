'''Предоставляется набор функций по взаимодействию с db проекта "Составление расписания"
Формат базы
Таблица пользователи            - users.
Таблица Список расписаний       - schedules
'''

#import sqlite3
#from sqlalchemy import create_engine
#from sqlalchemy import Column, Integer, String, Boolean, Text
#from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy.ext.declarative import declarative_base


#engine = create_engine('sqlite:///sched.db')
#db_session = scoped_session(sessionmaker(bind=engine))
#Base = declarative_base()
#Base.query = db_session.query_property()
#
#
#class User(Base):
#    __tablename__ = 'users'
#    id = Column(Integer, primary_key=True)
#    login = Column(String(50), unique=True)
#    isdeleted = Column(Boolean(True))
#
#    def __init__(self, login, isdeleted=False):
#        self.login = login
#        self.isdeleted = isdeleted
#
#    def __repr__(self):
#        return '<User {} {}>'.format(self.login, self.isdeleted)
#
#
##создаст базу если она не была создана
#Base.metadata.create_all(bind=engine)

#Интерфейс к базе

def add_user(login):
    '''Добавление пользователя в базу'''
    try:
        #u = User
        #check_user = u.query.filter(User.login == login).first()
        #if check_user:
        #    #пользоваетель есть
        #    if check_user.isdeleted:
        #
        #new_user = User(login,True)
        #db_session.add(new_user)
        #db_session.commit()
        #при ошибке вернуть False
        return True
    except:
        return False

def del_user(login):
    '''Удаление пользователя из базы'''
    #при ошибке вернуть False
    return True

#def add_duty(login, date):
#    '''Назначить пользователя на держурство'''
#    pass

