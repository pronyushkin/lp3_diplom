'''Предоставляется набор функций по взаимодействию с db проекта "Составление расписания"
Формат базы
Таблица пользователи             - users.
Таблица Списоки расписаний       - schedules
TODO убрать использование глобальных переменных (BASE_TYPE)
'''
#pip install sqlalchemy
#pylint: disable=maybe-no-member
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Boolean, Text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import update
import json

from schedule_exceptions import ScheduleException


BASE_TYPE = declarative_base()


class User(BASE_TYPE):
    '''Мапинг пользователей'''
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(Text, unique=True)
    isdeleted = Column(Boolean(False))

    def __init__(self, login, isdeleted=False):
        self.login = login
        self.isdeleted = isdeleted

    def __repr__(self):
        return '<User {} {}>'.format(self.login, self.isdeleted)


class Schedules(BASE_TYPE):
    '''Мапинг расписаний'''
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    month = Column(Integer, unique=True)
    schedule = Column(Text)

    def __init__(self, month, schedule=r'{}'):
        self.month = month
        self.schedule = schedule

    def __repr__(self):
        return '<Schedule {} {}>'.format(self.month, self.schedule)

    def __str__(self):
        return '({},{})'.format(self.month, self.schedule)


class SchedulesDb:
    '''Работа с базой данных расписаний'''
    def __init__(self, dbname):
        #TODO убрать глобальную BASE_TYPE
        global BASE_TYPE
        self.engine = create_engine('sqlite:///{}.db'.format(dbname))
        self.db_session = scoped_session(sessionmaker(bind=self.engine))
        BASE_TYPE.query = self.db_session.query_property()
        #создаст базу если она не была создана
        BASE_TYPE.metadata.create_all(bind=self.engine)

    #Вспомогательные
    def print_users(self, msg=''):
        '''Напечатать все записи о пользователях'''
        print('print_users', msg, User.query.all())


    def remove_user(self, vlogin):
        '''Удаление записи пользователя из базы'''
        User.query.filter_by(login=vlogin).delete()
        self.db_session.commit()


    def print_schedules(self, msg=''):
        '''Напечатать все записи о расписаниях'''
        print('print_schedules', msg, Schedules.query.all())


    #Интерфейс к базе
    def get_users(self):
        '''Получить текущий список пользователей'''
        logins_as_tuples = self.db_session.query(User.login).filter_by(isdeleted=False).all()
        logins = []
        for login in logins_as_tuples:
            logins.append(login[0])
        return logins


    def add_user(self, login):
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
                    self.db_session.commit()
                    return True
                else:
                    return False

            new_user = User(login, False)
            self.db_session.add(new_user)
            self.db_session.commit()
            return True
        except:
            print('except in add_user')
            return False


    def del_user(self, login):
        '''Удаление пользователя из базы'''
        try:
            u = User
            check_user = u.query.filter(User.login == login).first()
            if check_user:
                #пользователь есть
                if not check_user.isdeleted:
                    check_user.isdeleted = True
                    self.db_session.commit()
                    return True
            return False
        except:
            print('except in del_user')
            return False

    def delete_sched(self, month):
        '''Удалить расписание из базы'''
        try:
            Schedules.query.filter(Schedules.month == month).delete()
            self.db_session.commit()
            return True
        except:
            print('except in delete_sched')
            return False


    def update_sched(self, sched):
        '''Обновить расписание в базе'''
        assert(2 == len(sched))
        month, schedule = sched
        schedule = json.JSONEncoder().encode(schedule)
        try:
            s = Schedules
            check_sched = s.query.filter(Schedules.month == month).first()
            if check_sched:
                #расписание уже есть
                check_sched.schedule = schedule
                self.db_session.commit()
            else:
                new_sched = Schedules(month, schedule)
                self.db_session.add(new_sched)
                self.db_session.commit()
            return True
        except:
            print('except in update_sched')
            return False


    def get_schedules(self):
        '''Получить текущий набор расписаний'''
        scheds = self.db_session.query(Schedules).all()
        result = {}
        for i in scheds:
            obj = json.JSONDecoder().decode(i.schedule)
            converted_obj = {}
            for item in obj.items():
                converted_obj[int(item[0])] = item[1]
            result[i.month] = converted_obj
        return result


#проверки
def example_users(example_db):
    '''Примеры работы с таблицей пользователей'''
    print(example_db.get_users())
    print(example_db.add_user('test_user1'))
    print(example_db.add_user('test_user1'))#False
    print(example_db.add_user('test_user2_del'))
    print(example_db.add_user('test_user3'))
    example_db.print_users('3 ok users')
    print(example_db.del_user('test_user2_del'))
    print(example_db.get_users())
    example_db.print_users('2 ok users, 1 del user')
    print(example_db.del_user('notexists'))#False
    example_db.print_users('2 ok users, 1 del user')
    print(example_db.del_user('test_user3'))
    example_db.print_users('1 ok user, 2 del users')
    print(example_db.add_user('test_user3'))
    print(example_db.get_users())
    example_db.print_users('2 ok users, 1 del user')
    example_db.remove_user('test_user2_del')
    print(example_db.get_users())
    example_db.print_users('2 ok users')


def example_schedules(example_db):
    '''Примеры работы с таблицей расписаний'''
    print(example_db.get_schedules())
    example_db.update_sched((201611, {25:'user1', 28:'user2', 29:'user1', 30:'user2'}))
    print(example_db.get_schedules())
    example_db.update_sched((201611, {25:'user2', 28:'user2', 29:'user2', 30:'user2'}))
    print(example_db.get_schedules())
    example_db.update_sched((201612, {25:'user2', 28:'user2', 29:'user2', 30:'user2'}))
    print(example_db.get_schedules())


if __name__ == '__main__':
    main_db = SchedulesDb('test_sdb1')
    example_users(main_db)
    print('-'*80)
    example_schedules(main_db)
