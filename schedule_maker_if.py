"""
Интерфейс логики "Составление расписания"


pip install python-dateutil

pip install sqlalchemy

"""
import sys
from schedule_exceptions import ScheduleException
import schedule_maker as schm
if __name__ == '__main__':
    from datetime import datetime, date, timedelta


maker = None


def cmd_init(dbname = 'sched', istestmode = False):
    """
    Настраивает работу с указанной базой.
    """
    try:
        global maker
        maker = schm.ScheduleMaker(dbname, istestmode)
        return 'ok'
    except KeyboardInterrupt:
        raise
    except ScheduleException as e:
        return 'err in cmd_init {}'.format(e.msg)
    except:
        return 'err in cmd_init Unexpected {}'.format(sys.exc_info()[0])


def init_if_need():
    if not maker:
        cmd_init()


def cmd_remove_duty_by_day(day, schedule_id = None):
    """
    Убираем дежурства пользователя назначенного на указанный день.

    Находится день, определяется пользователь.
    Расписание сдвигается на один день, для последнего дня назначается новый пользователь в обычном порядке.
    Возвращает 'ok' в случае успеха или строку начинающуюся с 'err' с информацией об ошибке в противном случае.
    """
    try:
        init_if_need()
        return maker.remove_duty_by_day(day, schedule_id)
    except KeyboardInterrupt:
        raise
    except ScheduleException as e:
        return 'err in cmd_remove_duty_by_day {}'.format(e.msg)
    except:
        return 'err in cmd_remove_duty_by_day Unexpected {}'.format(sys.exc_info()[0])


def cmd_add_user(login):
    """
    Добавление пользователя.

    Возвращает 'ok' в случае успеха или строку начинающуюся с 'err' с информацией об ошибке в противном случае.

    """
    try:
        init_if_need()
        return maker.add_user(login)
    except KeyboardInterrupt:
        raise
    except ScheduleException as e:
        return 'err in cmd_add_user {}'.format(e.msg)
    except:
        return 'err in cmd_add_user Unexpected {}'.format(sys.exc_info()[0])


def cmd_del_user(login):
    """
    Удаление пользователя

    Возвращает 'ok' в случае успеха или строку начинающуюся с 'err' с информацией об ошибке в противном случае.
    """
    try:
        init_if_need()
        result = maker.del_user(login)
        #также снимаем его с будущих дежурств
        if 'ok' == result:
            maker.remove_future_update_this(None)

        return result
    except KeyboardInterrupt:
        raise
    except ScheduleException as e:
        return 'err in cmd_del_user {}'.format(e.msg)
    except:
        return 'err in cmd_del_user Unexpected {}'.format(sys.exc_info()[0])


def cmd_rebuild(schedule_id = None):
    """
    Удаляет будущие расписания и обновляет текущее

    Возвращает 'ok' в случае успеха или строку начинающуюся с 'err' с информацией об ошибке в противном случае.
    """
    try:
        init_if_need()
        maker.remove_future_update_this(schedule_id)
        return 'ok'
    except KeyboardInterrupt:
        raise
    except ScheduleException as e:
        return 'err in cmd_rebuild {}'.format(e.msg)
    except:
        return 'err in cmd_rebuild Unexpected {}'.format(sys.exc_info()[0])


def cmd_try_schedule(schedule_id = None):
    """
    Формируем расписание.
    И возвращаем его в требуемом виде.
    Результат не сохраняется.

    Возвращает расписание в виде строки '{1:'name1',2:'name2' ...,31:'namex'}'.
    При ошибке возвращает '{}'
    """
    try:
        init_if_need()
        sched = maker.make_schedule(schedule_id)
        return str(sched[1])
    except KeyboardInterrupt:
        raise
    except ScheduleException as e:
        return '{}'
    except:
        return '{}'


def cmd_make_schedule(schedule_id = None):
    """
    Формируем расписание.
    Сохраняем результат в базе.
    Возвращаем информацию о расписании.

    Возвращает расписание в виде строки '{1:'name1',2:'name2' ...,31:'namex'}'.
    При ошибке возвращает '{}'
    """
    try:
        init_if_need()
        sched_data = maker.make_schedule_and_save(schedule_id)
        return str(sched_data)
    except KeyboardInterrupt:
        raise
    except ScheduleException as e:
        return '{}'
    except:
        return '{}'


def cmd_show_schedule(schedule_id):
    """
    Извлекает информацию о существующем расписании и возвращает в требуемом виде.
    Пока принимаем дату в формате число вида YYYYMM например 201611
    В дальнейшем можно переделать на желаемый формат и преобразовывать к этому виду

    Возвращает расписание в виде строки '{1:'name1',2:'name2' ...,31:'namex'}'.
    Если не передана дата возвращает все расписания в виде строки '{{...},...{...}}'
    При ошибке возвращает '{}'
    """
    try:
        init_if_need()
        if schedule_id:
            sched = maker.schedules.get(schedule_id,{})
        else:
            sched = maker.schedules
        return str(sched)
    except KeyboardInterrupt:
        raise
    except ScheduleException as e:
        return '{}'
    except:
        return '{}'


if __name__ == '__main__':
    """Минимальное наполнение базы для тестирование с web интерфейсом"""
    try:
        raise ScheduleException('test exception')
    except ScheduleException as e:
        print('err {}'.format(e.msg))
    cmd_init()
    cmd_make_schedule()
    for i in range(1,5):
        user='u{}'.format(i)
        print(cmd_add_user(user))

