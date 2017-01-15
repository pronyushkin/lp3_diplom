'''Реализация логики "Составление расписания"'''
import schedule_db
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


class ScheduleMaker:
    '''
    Класс реализующий логику составления расписаний
    '''

    def __init__(self, dbname):
        self.db = schedule_db.SchedulesDb(dbname)
        #исходное состояние получаем из базы
        #список пользователей
        self.users = self.db.get_users()
        #словарь имеющихся расписаний
        #   ключ - годмесяц(YYYYMM), значение - словарь расписания на месяц
        #где:
        # словарь расписания на месяц
        #   ключ - число, значение пользователь
        self.schedules = self.db.get_schedules()


    def add_user(self,login):
        '''
        Добавляем пользователя
        '''
        if login in self.users:
            return 'err user {} exists'.format(login)

        if self.db.add_user(login):
            self.users.append(login)
            return 'ok'
        return 'err user {} addition failed'.format(login)


    def del_user(self,login):
        '''
        Удаляем пользователя
        '''
        if login not in self.users:
            return 'err user {} does not exist'.format(login)

        if self.db.del_user(login):
            self.users.remove(login)
            return 'ok'
        return 'err deleting user {} failed'.format(login)


    def check_prev(self, schedule_id, today):
        last_user = None
        prev = self.schedules.get(schedule_id,  None)
        if prev:
            checkday = today - 1
            while checkday:
                if not (checkday in prev.keys()):
                    break
                if prev[checkday] in self.users:
                    last_user = prev[today - 1]
                    break
                checkday -= 1
        return last_user


    def find_firstid(self,schedule_id, today):
        '''
        Ищем индекс пользователя который попадет в следующее расписание первым
        '''
        last_user = None
        #проверяем текущий месяц
        if 1 < today:
            last_user = self.check_prev(schedule_id, today)

        if not last_user:
            #проверяем предыдущий месяц (можно сделать цикл сколько надо)
            d = datetime(year=schedule_id//100, month=schedule_id%100, day = 1)
            d = d - timedelta(days=1)
            last_user = self.check_prev(schedule_id - 1, d.day + 1)

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


    def make_schedule(self, schedule_id):
        '''
        Формируем расписание.
        Расписание формируется от текущего дня и до конца месяца, либо от начала указанного месяца,
        при этом не рабочие дни не должны использоваться.
        Пример (201611:{25:'user1', 28:'user2',29:'user1', 30:'user2'} )
        Если месяц расписание уже было составлено то прошедшие дни не должны изменяться.
        '''
        nowday = datetime.today().date()
        now_id = nowday.year * 100 + nowday.month
        if not schedule_id:
            schedule_id = now_id

        if not len(self.users) or schedule_id < 201601:
            print('make_schedule wrong args')
            return (schedule_id, {})

        sch_dates = self.schedules.get(schedule_id,{})
        #на прошлые месяцы можно создавать только если еще не было
        if schedule_id < now_id and sch_dates != {}:
            return sch_dates

        if schedule_id != now_id:
            dit = datetime(year=schedule_id//100, month=schedule_id%100, day = 1)
        else:
            dit = nowday

        next_month_begin = dit + relativedelta(months=1)
        next_month_begin = next_month_begin.replace(day = 1)

        user_id = self.find_firstid(schedule_id,dit.day)
        user_lim = len(self.users)
        while dit < next_month_begin:
            if self.is_workday(dit):
                sch_dates[dit.day] = self.users[user_id % user_lim]
                user_id += 1
            dit = (dit + timedelta(days=1))
        return (schedule_id, sch_dates)


    def make_schedule_and_save(self, schedule_id):
        '''
        Формируем расписание и сохраняем его.
        '''
        sched = self.make_schedule(schedule_id)
        if not self.db.update_sched(sched):
            return {}
        self.schedules[sched[0]] = sched[1]
        return sched[1]


    def remove_duty_by_day(self,day):
        '''
        Сдвинуть график дежурств.

        Находится день.
        Расписание сдвигается на один день, для последнего дня назначается новый пользователь в обычном порядке.
        Возвращает 'ok' в случае успеха или строку начинающуюся с 'err' с информацией об ошибке в противном случае.
        '''
        return 'ok'


    def remove_duty_by_user(self,login):
        '''
        Удаление всех дежурств оставшихся у этого пользователя в этом месяце
        '''
        return 'ok'


if __name__ == '__main__':
    schedule_maker = ScheduleMaker('test_schedule_maker')
    print(schedule_maker.add_user('testuser1'))
    print(schedule_maker.add_user('testuser2'))
    print(schedule_maker.make_schedule(201601))
