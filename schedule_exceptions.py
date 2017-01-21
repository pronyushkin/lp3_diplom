'''
Исключения проекта "Составление расписания"
'''

class ScheduleException(Exception):
    '''
    Базовый класс исключений проекта "Составление расписания"
    '''

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

