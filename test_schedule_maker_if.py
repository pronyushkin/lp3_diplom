'''
Тест интерфейса логики "Составление расписания"

py.test -s test_schedule_maker_if.py
'''

import pytest
import os
import uuid
import schedule_maker_if as schm

dbname = 'test_if{}'.format(uuid.uuid4())


def teardown_module(module):
    '''Удалить тестовую базу'''
    print('pytest teardown_module', module)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), dbname + '.db')
    if os.path.exists(path):
        os.remove(path)


def setup_module(module):
    '''Подключиться к тестовой базе'''
    print('pytest setup_module', module)
    teardown_module(module)
    schm.cmd_init(dbname, True)


def test_schedule_maker_if_users():
    '''Тест работы с пользователями'''
    cu = []
    #добавление
    assert('ok' == schm.cmd_add_user('u1'))
    cu.append('u1')
    assert(schm.maker.users == cu)

    schm.cmd_add_user('u_del')
    cu.append('u_del')
    assert(schm.maker.users == cu)

    for i in range(2,9):
        user='u{}'.format(i)
        assert('ok' == schm.cmd_add_user(user))
        cu.append(user)
        assert(schm.maker.users == cu)

    #удаление пользователя
    assert('ok' == schm.cmd_del_user('u_del'))
    del cu[1]#u_del

    #неуспешная попытка добавления существующего пользователя
    assert('ok' != schm.cmd_add_user('u3'))
    print('users', schm.maker.users)

    #очищаем
    for u in cu:
        assert('ok' == schm.cmd_del_user(u))
    print('users', schm.maker.users)


def test_schedule_maker_if_sched():
    '''Тест работы c расписаниями'''
    #исходное состояние чистое
    assert( [] == schm.maker.users)
    assert( {} == schm.maker.schedules)

    #добавление пользователей
    cu = []
    for i in range(1,5):
        user='u{}'.format(i)
        assert('ok' == schm.cmd_add_user(user))
        cu.append(user)
        assert(schm.maker.users == cu)

    print(schm.maker.users)

    ctrl1 = {
         1: 'u1',  2: 'u2',  3: 'u3',  4: 'u4',
         7: 'u1',  8: 'u2',  9: 'u3', 10: 'u4',
        11: 'u1', 14: 'u2', 15: 'u3', 16: 'u4',
        17: 'u1', 18: 'u2', 21: 'u3', 22: 'u4',
        23: 'u1', 24: 'u2', 25: 'u3', 28: 'u4',
        29: 'u1', 30: 'u2'}

    sch1 = schm.cmd_try_schedule(201611)
    assert(sch1 == str(ctrl1))
    assert(sch1 == schm.cmd_make_schedule(201611))
    ctrl2 = {
         1: 'u3',  2: 'u4',
         5: 'u1',  6: 'u2',  7: 'u3',  8: 'u4',
         9: 'u1', 12: 'u2', 13: 'u3', 14: 'u4',
        15: 'u1', 16: 'u2', 19: 'u3', 20: 'u4',
        21: 'u1', 22: 'u2', 23: 'u3', 26: 'u4',
        27: 'u1', 28: 'u2', 29: 'u3', 30: 'u4'}
    assert(str(ctrl2) == schm.cmd_make_schedule(201612))

    #поскольку выставлен флаг тест сегодня 2016/09/15
    ctrl3 = {
        15: 'u1', 16: 'u2', 19: 'u3', 20: 'u4',
        21: 'u1', 22: 'u2', 23: 'u3', 26: 'u4',
        27: 'u1', 28: 'u2', 29: 'u3', 30: 'u4'}
    assert(str(ctrl3) == schm.cmd_make_schedule())
    assert('ok' == schm.cmd_remove_duty_by_day(19))
    ctrl4 = {
        15: 'u1', 16: 'u2',           19: 'u4',
        20: 'u1', 21: 'u2', 22: 'u3', 23: 'u4',
        26: 'u1', 27: 'u2', 28: 'u3', 29: 'u4',
        30: 'u1'}
    assert(str(ctrl4) == schm.cmd_show_schedule(201609))
    assert('ok' != schm.cmd_remove_duty_by_day(14))

    assert(str({}) == schm.cmd_show_schedule(201710))

    #печать имеющихся расписаний
    print('showAll', schm.cmd_show_schedule(None))
    #очищаем
    ctrl5 = {
        15: 'u4', 16: 'u4',           19: 'u4',
        20: 'u4', 21: 'u4', 22: 'u4', 23: 'u4',
        26: 'u4', 27: 'u4', 28: 'u4', 29: 'u4',
        30: 'u4'}    
    for u in cu:
        if 1 == len(cu):
            #убеждаемся что при удалении пользователей обновляется расписание
            assert(str(ctrl5) == schm.cmd_show_schedule(201609))
        #удаляем пользователя
        assert('ok' == schm.cmd_del_user(u))


if __name__ == '__main__':
    '''Проверки'''
    setup_module(__file__)
    test_schedule_maker_if_users()
    test_schedule_maker_if_all()
    teardown_module(__file__)
