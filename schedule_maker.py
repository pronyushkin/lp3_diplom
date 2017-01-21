'''Реализация логики "Составление расписания"'''
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import schedule_db


class ScheduleMaker:
    '''
    Класс реализующий логику составления расписаний
    '''

    def __init__(self, dbname, istestmode=False):
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
        self.istestmode = istestmode


    def get_now(self):
        '''
        Получение текущей даты и индекса расписания текущего месяца
        '''
        if self.istestmode:
            #для тестов нужно чтобы дата была одинаковая чтобы совпадала с тестовыми данными
            sch_day = datetime(year=2016, month=9, day=15)
        else:
            sch_day = datetime.today().date()

        now_id = sch_day.year * 100 + sch_day.month
        return (now_id, sch_day)


    def add_user(self, login):
        '''
        Добавляем пользователя
        '''
        if login in self.users:
            return 'err user {} exists'.format(login)

        if self.db.add_user(login):
            self.users.append(login)
            return 'ok'
        return 'err user {} addition failed'.format(login)


    def del_user(self, login):
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
        '''
        Проверить предыдущее расписание
        '''
        last_user = None
        prev = self.schedules.get(schedule_id, None)
        if prev:
            checkday = today - 1
            while checkday:
                if not checkday in prev.keys():
                    break
                if prev[checkday] in self.users:
                    last_user = prev[today - 1]
                    break
                checkday -= 1
        return last_user


    def find_firstid(self, schedule_id, today):
        '''
        Ищем индекс пользователя который попадет в следующее расписание первым
        '''
        last_user = None
        #проверяем текущий месяц
        if today > 1:
            last_user = self.check_prev(schedule_id, today)

        if not last_user:
            #проверяем предыдущий месяц (можно сделать цикл сколько надо)
            last_date = datetime(year=schedule_id//100, month=schedule_id%100, day=1)
            last_date = last_date - timedelta(days=1)
            last_user = self.check_prev(schedule_id - 1, last_date.day + 1)

        #если предыдущий пользователь найден возвращаем следующий индекс
        if last_user:
            return self.users.index(last_user) + 1
        #пользователь не найден начинаем сначала
        return 0


    def is_workday(self, dit):
        '''
        Определить является ли дата рабочим днем
        TODO добавить возможность настройки дополнительных рабочих и не рабочих дней
        для этого можно завести еще два списка, рабочих и не рабочих дней и функции для управления
        ими пока отбрасываем только субботы, воскресенья
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
        now_id, nowday = self.get_now()

        if not schedule_id:
            schedule_id = now_id

        if schedule_id > now_id + 100 :
            return (schedule_id, {})

        if not len(self.users) or schedule_id < 201601:
            print('make_schedule wrong args')
            return (schedule_id, {})

        sch_dates = self.schedules.get(schedule_id, {})
        #на прошлые месяцы можно создавать только если еще не было
        if schedule_id < now_id and sch_dates != {}:
            return sch_dates

        if schedule_id != now_id:
            dit = datetime(year=schedule_id//100, month=schedule_id%100, day=1)
        else:
            dit = nowday

        next_month_begin = dit + relativedelta(months=1)
        next_month_begin = next_month_begin.replace(day=1)

        user_id = self.find_firstid(schedule_id, dit.day)
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


    def remove_duty_by_day(self, rmday, schedule_id):
        '''
        Сдвинуть график дежурств.

        Находится день.
        Расписание сдвигается на один день,
        для последнего дня назначается новый пользователь в обычном порядке.
        Возвращает 'ok' в случае успеха или строку начинающуюся с
        'err' с информацией об ошибке в противном случае.
        '''
        now_id, nowday = self.get_now()
        if not schedule_id:
            schedule_id = now_id
        if schedule_id < now_id:
            return 'err can not to change past'
        if now_id == schedule_id and nowday.day >= rmday:
            return 'err can not to change past'

        sched = self.schedules.get(schedule_id, None)
        if not sched:
            return 'err have no schedule'

        if not len(sched):
            return 'err schedule is empty'

        if not rmday in sched:
            return 'err day in not in schedule'

        days = sorted(sched.keys())
        i = days.index(rmday)
        while i + 1 < len(days):
            sched[days[i]] = sched[days[i+1]]
            i += 1

        last_user_id = self.users.index(sched[days[-2]])
        user_lim = len(self.users)
        user_id = (last_user_id + 1) % user_lim
        sched[days[-1]] = self.users[user_id]
        if not self.db.update_sched((schedule_id, sched)):
            return 'err updatedb'
        return 'ok'


    def remove_future_update_this(self):
        '''
        Удаление расписаний на будущие месяцы
        Перегенерация текущего если надо
        '''
        now_id, nowday = self.get_now()
        for sched_id in self.schedules:
            if now_id < sched_id:
                self.db.delete_sched(sched_id)
        if now_id in self.schedules:
            self.make_schedule_and_save(None)
