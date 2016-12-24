'''Реализация логики "Составление расписания"'''
import schedule_db


class ScheduleMaker:
	def __init__(self):
		#todo формировать словари из базы данных
		#пока тестовое заполнение чтобы понять что хотим получит
		#список пользователей
		self.users = ['user1','user2']
		#словарь имеющихся расписаний 
		#	ключ - годмесяц, значение - словарь расписания на месяц
		#словарь расписания на месяц это набо
		#	ключ - число, значение пользователь
		self.schedules = { 
			201612:{26:'user1', 27:'user2',28:'user1', 29:'user2', 30:'user1'},
			201611:{25:'user1', 28:'user2',29:'user1', 30:'user2'}
		}


	def add_user(self,login):
		'''
		Добавляем пользователя
		'''
		if login in self.users:
			return 'err user {} exists'.format(login)

		if schedule_db.add_user(login):
			self.users.append(login)
			return 'ok'
		return 'err adding user {} failed'.format(login)

	def del_user(self,login):
		'''
		Удаляем пользователя
		'''
		if login not in self.users:
			return 'err user {} do not exists'.format(login)

		if schedule_db.del_user(login):
			self.users.remove(login)
			return 'ok'
		return 'err deleting user {} failed'.format(login)


	def make_schedule(self):
		'''
		Формируем расписание.
		Расписание формируется от текущего дня и до конца месяца, 
		при этом не рабочие дни не должны использоваться.
		'''
		pass



schedule_maker = ScheduleMaker()
