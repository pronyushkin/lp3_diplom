'''
Интерфейс логики "Составление расписания"


pip install python-dateutil

pip install sqlalchemy

'''

import schedule_maker as schm
if __name__ == '__main__':
    from datetime import datetime, date, timedelta


maker = None

def cmd_init(dbname = 'sched', istestmode = False):
    '''
    Настраивает работу с указанной базой.
    '''
    global maker
    maker = schm.ScheduleMaker(dbname, istestmode)


def init_if_need():
    if not maker:
        cmd_init()


def cmd_remove_duty_by_day(day):
    '''
    Убираем дежурства пользователя назначенного на указанный день.

    Находится день, определяется пользователь.
    Расписание сдвигается на один день, для последнего дня назначается новый пользователь в обычном порядке.
    Возвращает 'ok' в случае успеха или строку начинающуюся с 'err' с информацией об ошибке в противном случае.
    '''
    init_if_need()
    return maker.remove_duty_by_day(day, None)


def cmd_add_user(login):
    '''
    Добавление пользователя.

    Возвращает 'ok' в случае успеха или строку начинающуюся с 'err' с информацией об ошибке в противном случае.

    '''
    init_if_need()
    return maker.add_user(login)


def cmd_del_user(login):
    '''
    Удаление пользователя

    Возвращает 'ok' в случае успеха или строку начинающуюся с 'err' с информацией об ошибке в противном случае.
    '''
    init_if_need()
    result = maker.del_user(login)
    #также снимаем его с будущих дежурств
    if 'ok' == result:
        maker.remove_duty_by_user(login)
    return result


def cmd_try_schedule(schedule_date = None):
    '''
    Формируем расписание.
    И возвращаем его в требуемом виде.
    Результат не сохраняется.

    Возвращает расписание в виде строки '{1:'name1',2:'name2' ...,31:'namex'}'.

    '''
    init_if_need()
    sched = maker.make_schedule(schedule_date)
    return str(sched[1])


def cmd_make_schedule(schedule_date = None):
    '''
    Формируем расписание.
    Сохраняем результат в базе.
    Возвращаем информацию о расписании.

    Возвращает расписание в виде строки '{1:'name1',2:'name2' ...,31:'namex'}'.
    '''
    init_if_need()
    sched_data = maker.make_schedule_and_save(schedule_date)
    return str(sched_data)


def cmd_show_schedule(schedule_date):
    '''
    Извлекает информацию о существующем расписании и возвращает в требуемом виде.
    Пока принимаем дату в формате число вида YYYYMM например 201611
    В дальнейшем можно переделать на желаемый формат и преобразовывать к этому виду

    Возвращает расписание в виде строки '{1:'name1',2:'name2' ...,31:'namex'}'.
    '''
    init_if_need()
    if schedule_date:
        sched = maker.schedules.get(schedule_date,{})
    else:
        sched = maker.schedules
    return str(sched)
