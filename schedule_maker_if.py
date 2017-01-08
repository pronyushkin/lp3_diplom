'''Интерфейс логики "Составление расписания"'''
#import schedule_maker

import schedule_maker as schm

def cmd_add_user(login):
    '''
    Добавление пользователя.
    '''
    return schm.schedule_maker.add_user(login)


def cmd_del_user(login):
    '''
    Удаление пользователя
    Удаляем из базы пользователя и все назначенные ему дежурства.
    '''
    return schm.schedule_maker.del_user(login)


def cmd_try_schedule():
    '''
    Формируем расписание.
    И возвращаем его в требуемом виде.
    Результат не сохраняется.
    '''
    sched = schm.schedule_maker.make_schedule()
    return str(sched[1])


def cmd_make_schedule():
    '''
    Формируем расписание.
    Сохраняем результат в базе.
    Возвращаем информацию о расписании.
    '''
    sched_data = schm.schedule_maker.make_schedule_and_save()
    return str(sched_data)

def cmd_show_schedule(schedule_date):
    '''
    Извлекает из информацию о существующем расписании и возвращает в требуемом виде.
    Пока принимаем дату в формате число вида YYYYMM например 201611
    В дальнейшем можно переделать на желаемый формат и приобразовывать к этому виду
    '''
    if schedule_date:
        sched = schm.schedule_maker.schedules.get(schedule_date,{})
    else:
        sched = schm.schedule_maker.schedules    
    return str(sched)


if __name__ == '__main__':
    '''тестовый прогон'''
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

