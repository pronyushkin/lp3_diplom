'''Реализация логики "Составление расписания"'''
import schedule_db
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

class ScheduleMaker:
    def __init__(self):
        #todo формировать словари из базы данных
        #пока тестовое заполнение чтобы понять что хотим получит
        #список пользователей
        self.users = ['user1','user2']
        #словарь имеющихся расписаний 
        #   ключ - годмесяц, значение - словарь расписания на месяц
        #словарь расписания на месяц это набо
        #   ключ - число, значение пользователь
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
        Пример (201611:{25:'user1', 28:'user2',29:'user1', 30:'user2'} )
        '''
        dit = datetime.today()
        #для проверки с любого дня раскоментировать строку ниже и установить там день
        #dit = dit.replace(day = 15)
        schedule_id = dit.year * 100 + dit.month
        next_month_begin = datetime.today() + relativedelta(months=1)
        next_month_begin = next_month_begin.replace(day = 1)
        sch_dates = {}
        user_id = 0 #TODO вычислить с учетом предыдущего расписания, либо предыдущей версии этого
        user_lim = len(self.users)
        while dit < next_month_begin:
            if not (dit.weekday() == 5 or dit.weekday() == 6):
                sch_dates[dit.day] = self.users[user_id % user_lim]
                user_id += 1
            dit = (dit + timedelta(days=1))
        return (schedule_id,sch_dates)

    def make_schedule_and_save(self):
        '''
        Формируем расписание и сохраняем его.
        '''
        sched = self.make_schedule()
        #TODO сохранить в базе
        self.schedules[sched[0]] = sched[1]
        return sched[1]


schedule_maker = ScheduleMaker()
