'''Интерфейс логики "Составление расписания"'''
#import schedule_maker

import schedule_maker

def cmd_add_user(login):
    '''
    Добавление пользователя.
    Только добавляем пользователя в базу.
    '''
    #schedule_db.add_user(login)
    pass


def cmd_del_user(login):
    '''Удаление пользователя
    Удаляем из базы пользователя и все назначенные ему дежурства.
    '''
    pass


def cmd_try_schedule():
    '''
    Формируем расписание.
    И возвращаем его в требуемом виде.
    Результат не сохраняется.
    '''
    pass


def cmd_make_schedule():
    '''
    Формируем расписание.
    Сохраняем результат в базе.
    Возвращаем информацию о расписании.
    '''
    pass

def cmd_show_schedule(schedule_date):
    '''
    Извлекает из информацию о существующем расписании и возвращает в требуемом виде.
    Пока принимаем дату в формате число вида YYYYMM например 201611
    В дальнейшем можно переделать на желаемый формат и приобразовывать к этому виду
    '''
    sched = str(schedule_maker.schedule_maker.schedules.get(schedule_date,{}))
    return sched

if __name__ == '__main__':
    '''тестовый прогон'''
    #cmd_add_user('вася')
    #cmd_add_user('петя')
    #cmd_add_user('удаляка')
    #cmd_add_user('леша')
    #cmd_add_user('ваня')
    #cmd_add_user('варя')
    #cmd_add_user('поля')
    #cmd_add_user('коля')
    #cmd_add_user('леня')
    #print(cmd_try_schedule())
    #cmd_del_user('удаляка')
    #print(cmd_make_schedule())
    #print(cmd_show_schedule(schedule_date))
    print(cmd_show_schedule(201610))
    print(cmd_show_schedule(201611))
    print(cmd_show_schedule(201612))

