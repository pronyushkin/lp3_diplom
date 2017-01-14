'''
Интерфейс логики "Составление расписания"


pip install python-dateutil

pip install sqlalchemy

'''

import schedule_maker as schm


def cmd_remove_duty_by_day(day):
    '''
    Убираем дежурства пользователя назначенного на указанный день.

    Находится день, определяется пользователь. 
    Расписание сдвигается на один день, для последнего дня назначается новый пользователь в обычном порядке.
    Возвращает 'ok' в случае успеха или строку начинающуюся с 'err' с информацией об ошибке в противном случае.
    '''
    return schm.schedule_maker.remove_duty_by_day(day)


def cmd_add_user(login):
    '''
    Добавление пользователя.

    Возвращает 'ok' в случае успеха или строку начинающуюся с 'err' с информацией об ошибке в противном случае.

    '''
    return schm.schedule_maker.add_user(login)


def cmd_del_user(login):
    '''
    Удаление пользователя

    Возвращает 'ok' в случае успеха или строку начинающуюся с 'err' с информацией об ошибке в противном случае.
    '''
    result = schm.schedule_maker.del_user(login)
    #также снимаем его с будущих дежурств
    if 'ok' == result:
        schm.schedule_maker.remove_duty_by_user(login)
    return result


def cmd_try_schedule(schedule_date = None):
    '''
    Формируем расписание.
    И возвращаем его в требуемом виде.
    Результат не сохраняется.

    Возвращает расписание в виде строки '{1:'name1',2:'name2' ...,31:'namex'}'.

    '''
    sched = schm.schedule_maker.make_schedule(schedule_date)
    return str(sched[1])


def cmd_make_schedule(schedule_date = None):
    '''
    Формируем расписание.
    Сохраняем результат в базе.
    Возвращаем информацию о расписании.

    Возвращает расписание в виде строки '{1:'name1',2:'name2' ...,31:'namex'}'.
    '''
    sched_data = schm.schedule_maker.make_schedule_and_save(schedule_date)
    return str(sched_data)


def cmd_show_schedule(schedule_date):
    '''
    Извлекает из информацию о существующем расписании и возвращает в требуемом виде.
    Пока принимаем дату в формате число вида YYYYMM например 201611
    В дальнейшем можно переделать на желаемый формат и преобразовывать к этому виду

    Возвращает расписание в виде строки '{1:'name1',2:'name2' ...,31:'namex'}'.
    '''
    if schedule_date:
        sched = schm.schedule_maker.schedules.get(schedule_date,{})
    else:
        sched = schm.schedule_maker.schedules    
    return str(sched)


def test_piv():
    '''Тестовый прогон'''
    #исходное состояние расписания
    print('showAll', cmd_show_schedule(None))
    #успешное добавление пользователей
    print(cmd_add_user('вася'))
    print(cmd_add_user('петя'))
    print(cmd_add_user('удаляка'))
    print(cmd_add_user('леша'))
    print(cmd_add_user('ваня'))
    print(cmd_add_user('варя'))
    print(cmd_add_user('поля'))
    print(cmd_add_user('коля'))
    print(cmd_add_user('леня'))
    print(schm.schedule_maker.users)
    #неуспешная попытка добавления существующего пользователя
    print(cmd_add_user('леня'))
    print('users', schm.schedule_maker.users)
    print('try',cmd_try_schedule())
    #удаление пользователя
    cmd_del_user('удаляка')
    print('users',schm.schedule_maker.users)
    print('make', cmd_make_schedule())
    print('show201701', cmd_show_schedule(201701))
    #печать имеющихся словарей
    print('showAll', cmd_show_schedule(None))


if __name__ == '__main__':
    '''Проверки'''
    test_piv()
