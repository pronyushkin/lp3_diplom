'''Реализация логики "Составление расписания"'''
import schedule_db
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


class ScheduleMaker:
    '''
    Класс реализующий логику составления расписаний
    '''

    def __init__(self):
        #исходное состояние получаем из базы
        #список пользователей
        self.users = schedule_db.get_users()
        #словарь имеющихся расписаний 
        #   ключ - годмесяц, значение - словарь расписания на месяц
        #где:
        # словарь расписания на месяц
        #   ключ - число, значение пользователь
        self.schedules = schedule_db.get_schedules()


    def add_user(self,login):
        '''
        Добавляем пользователя
        '''
        if login in self.users:
            return 'err user {} exists'.format(login)

        if schedule_db.add_user(login):
            self.users.append(login)
            return 'ok'
        return 'err user {} addition failed'.format(login)


    def del_user(self,login):
        '''
        Удаляем пользователя
        '''
        if login not in self.users:
            return 'err user {} does not exist'.format(login)

        if schedule_db.del_user(login):
            self.users.remove(login)
            return 'ok'
        return 'err deleting user {} failed'.format(login)


    def find_firstid(self,schedule_id, today, iteration = 1):
        '''
        Ищем индекс пользователя который попадет в следующее расписание первым
        '''
        #TODO вычислить с учетом предыдущего расписания, либо предыдущей версии этого
        prev = self.schedules.get(schedule_id,  None)
        last_user = None
        if prev:
            checkday = today - 1 
            while checkday:
                if prev[checkday] in self.users:
                    last_user = prev[today - 1]
                    break
                checkday -= 1
        elif iteration:
            iteration -= 1
            #делаем попытку проверить предыдущий месяц 
            #(количество попыток можно увеличить настройкой значения по умолчанию)
            #если сделали достаточно попыток то можно начинать сначала
            return self.find_firstid(schedule_id - 1, 1, iteration)
        #если предыдущий пользователь найден возвращаем следующий индекс
        if last_user:
            return self.users.index(last_user) + 1
        #пользователь не найден начинаем сначала
        return 0


    def is_workday(self,dit):
        '''
        Определить является ли дата рабочим днем
        TODO добавить возможность настройки дополнительных рабочих и не рабочих дней
        для этого можно завести еще два списка, рабочих и не рабочих дней и функции для управления ими
        пока отбрасываем только субботы, воскресенья
        '''
        if dit.weekday() == 5 or dit.weekday() == 6:
            return False
        return True


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
        user_id = self.find_firstid(schedule_id,dit.day)
        user_lim = len(self.users)
        while dit < next_month_begin:
            if self.is_workday(dit):
                sch_dates[dit.day] = self.users[user_id % user_lim]
                user_id += 1
            dit = (dit + timedelta(days=1))
        return (schedule_id, sch_dates)


    def make_schedule_and_save(self):
        '''
        Формируем расписание и сохраняем его.
        '''
        sched = self.make_schedule()
        if not schedule_db.update_sched(sched):
            return {}
        self.schedules[sched[0]] = sched[1]
        return sched[1]


schedule_maker = ScheduleMaker()
