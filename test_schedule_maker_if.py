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
    print('pytest teardown_module', module)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), dbname + '.db')
    if os.path.exists(path):
        os.remove(path)

        
def setup_module(module):
    print('pytest setup_module', module)
    print('pytest teardown_module', module)
    schm.cmd_init(dbname)

    
def test_schedule_maker_if_all():
    '''Тестовый прогон'''
    #исходное состояние расписания
    print('showAll', schm.cmd_show_schedule(None))
    #успешное добавление пользователей
    cu = []
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

    print(schm.maker.users)
    #неуспешная попытка добавления существующего пользователя
    assert('ok' != schm.cmd_add_user('u3'))
    print('users', schm.maker.users)
    print('try',schm.cmd_try_schedule())
    test_schm = {1: 'u1', 2: 'u_del', 5: 'u2', 6: 'u3', 7: 'u4', 8: 'u5', 9: 'u6', 12: 'u7', 13: 'u8', 14: 'u1', 15: 'u_del', 16: 'u2', 19: 'u3', 20: 'u4', 21: 'u5', 22: 'u6', 23: 'u7', 26: 'u8', 27: 'u1', 28: 'u_del', 29: 'u2', 30: 'u3'}
    test_schm_try = schm.cmd_try_schedule(201612)
    assert(str(test_schm) == test_schm_try)
    #удаление пользователя
    schm.cmd_del_user('u_del')
    del cu[1]#u_del
    assert(schm.maker.users == cu)
    print('make', schm.cmd_make_schedule())
    print('show201701', schm.cmd_show_schedule(201701))
    print('try 201702',schm.cmd_try_schedule(201702))
    #печать имеющихся словарей
    print('showAll', schm.cmd_show_schedule(None))


if __name__ == '__main__':
    '''Проверки'''
    setup_module('')
    test_schedule_maker_if_all()
    teardown_module('')
