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


#Интерфейс к базе

def get_users():
    '''Получить текущий список пользователей'''
    raw_users = User.query.filter_by(isdeleted=False).all()
    logins = []
    for raw_user in raw_users:
        logins.append(raw_user.login)
    return logins


def add_user(login):
    '''Добавление пользователя в базу'''
    try:
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
        return False


def update_sched(sched):
    '''Обновить расписание в базе'''
    return True


def get_schedules():
    '''Получить текущий набор расписаний'''
    return { 
            201612:{26:'user1', 27:'user2',28:'user1', 29:'user2', 30:'user1'},
            201611:{25:'user1', 28:'user2',29:'user1', 30:'user2'}
    }


if __name__ == '__main__':
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

