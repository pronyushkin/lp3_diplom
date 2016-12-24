'''Предоставляется набор функций по взаимодействию с db проекта "Составление расписания"
Формат базы
Таблица пользователи			- users.
Таблица Список расписаний       - schedules
Таблица Информация расписаний   - sch_data
'''

import sqlite3





def create_db_ifneed():
	'''Проверяет наличие файла базы данных и создает её если надо'''
	pass


def add_user(login):
	'''Добавление пользователя в базу'''
	#sql_request = 'insert into users {};'.format(login)
	#при ошибке вернуть False
	return True

def del_user(login):
	'''Удаление пользователя из базы'''
	#при ошибке вернуть False
	return True

def add_duty(login, date):
	'''Назначить пользователя на держурство'''
	pass

if __name__ == '__main__':
    create_db_ifneed()

