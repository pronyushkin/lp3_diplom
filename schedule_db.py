'''Предоставляется набор функций по взаимодействию с db проекта "Составление расписания"
Формат базы
Таблица пользователи             - users.
Таблица Списоки расписаний       - schedules
'''
#pip install sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import update
import json


engine = create_engine('sqlite:///sched.db')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(Text, unique=True)
    isdeleted = Column(Boolean(False))

    def __init__(self, login, isdeleted=False):
        self.login = login
        self.isdeleted = isdeleted

    def __repr__(self):
        return '<User {} {}>'.format(self.login, self.isdeleted)


class Schedules(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    month = Column(Integer, unique=True)
    schedule = Column(Text)

    def __init__(self, month, schedule='\{\}'):
        self.month = month
        self.schedule = schedule

    def __repr__(self):
        return '<Schedule {} {}>'.format(self.month, self.schedule)

    def __str__(self):
        return '({},{})'.format(self.month, self.schedule)


#создаст базу если она не была создана
Base.metadata.create_all(bind=engine)

#Вспомогательные

def print_users(msg=''):
    '''Напечатать все записи о пользователях'''
    print('print_users', msg, User.query.all())


def remove_user(vlogin):
    '''Удаление записи пользователя из базы'''
    User.query.filter_by(login=vlogin).delete()
    db_session.commit()


def print_schedules(msg=''):
    '''Напечатать все записи о расписаниях'''
    print('print_schedules', msg, Schedules.query.all())


#Интерфейс к базе

def get_users():
    '''Получить текущий список пользователей'''
    logins_as_tuples = db_session.query(User.login).filter_by(isdeleted=False).all()
    logins = []
    for login in logins_as_tuples:
        logins.append(login[0])
    return logins


def add_user(login):
    '''Добавление пользователя в базу'''
    try:
        #sqlalchemy сам экранирует символы
        #login = login.remove("'")
        #login = login.remove('"')
        u = User
        check_user = u.query.filter(User.login == login).first()
        if check_user:
            #пользоваетель есть
            if check_user.isdeleted:
                check_user.isdeleted = False
                db_session.commit()
                return True
            else:
                return False
        
        new_user = User(login, False)
        db_session.add(new_user)
        db_session.commit()
        return True
    except:
        print('except in add_user')
        return False


def del_user(login):
    '''Удаление пользователя из базы'''
    try:
        u = User
        check_user = u.query.filter(User.login == login).first()
        if check_user:
            #пользоваетель есть
            if not check_user.isdeleted:
                check_user.isdeleted = True
                db_session.commit()
                return True
        return False
    except:
        print('except in del_user')
        return False


def update_sched(sched):
    '''Обновить расписание в базе'''
    assert( 2 == len(sched))
    month, schedule = sched
    schedule = json.JSONEncoder().encode(schedule)
    try:
        s = Schedules
        check_sched = s.query.filter(Schedules.month == month).first()
        if check_sched:
            #расписание уже есть
            check_sched.schedule = schedule
            db_session.commit()
        else:
            new_sched= Schedules(month, schedule)
            db_session.add(new_sched)
            db_session.commit()
        return True
    except:
        print('except in update_sched')
        return False


def get_schedules():
    '''Получить текущий набор расписаний'''
    scheds = db_session.query(Schedules).all()
    result = {}
    for i in scheds:
        obj = json.JSONDecoder().decode(i.schedule)
        converted_obj = {}
        for item in obj.items():
            converted_obj[int(item[0])] = item[1]
        result[i.month] = converted_obj
    return result


#проверки
def example_users():
    '''Примеры работы с таблицей пользователей'''
    print(get_users())
    print(add_user('test_user1'))
    print(add_user('test_user1'))#False
    print(add_user('test_user2_del'))
    print(add_user('test_user3'))
    print_users('3 ok users')
    print(del_user('test_user2_del'))
    print(get_users())
    print_users('2 ok users, 1 del user')
    print(del_user('notexists'))#False
    print_users('2 ok users, 1 del user')
    print(del_user('test_user3'))
    print_users('1 ok user, 2 del users')
    print(add_user('test_user3'))
    print(get_users())
    print_users('2 ok users, 1 del user')
    remove_user('test_user2_del')
    print(get_users())
    print_users('2 ok users')


def example_schedules():
    '''Примеры работы с таблицей расписаний'''
    print(get_schedules())
    update_sched((201611,{25:'user1', 28:'user2',29:'user1', 30:'user2'} ))
    print(get_schedules())
    update_sched((201611,{25:'user2', 28:'user2',29:'user2', 30:'user2'} ))
    print(get_schedules())
    update_sched((201612,{25:'user2', 28:'user2',29:'user2', 30:'user2'} ))
    print(get_schedules())


if __name__ == '__main__':
    example_users()
    print('-'*80)
    example_schedules()
