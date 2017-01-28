import sys
from flask import Flask, render_template, request
import datetime
from calendar import Calendar
import yaml
import locale
import schedule_maker_if


def setup_locale(platform):
    if platform == 'win32':
        locale.setlocale(locale.LC_ALL, 'ru')
    elif platform == 'linux':
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

def process_month(date):
    month = date.strftime("%B")
    year = date.strftime("%Y")
#    week = datetime.date(date.year, date.month, 1).strftime("%W")

    cal = Calendar().monthdatescalendar(date.year, date.month)

    days = []
    for calweek in cal:
        week = []

        for calday in calweek:
            if calday.month == date.month:
#                week.append(calday)
                week.append(int(calday.strftime("%d")))
            else:
#                week.append(None)
                week.append('')

        days.append(week)

    return {
        'month': month,
        'year': year,
        'days': days
    }

schedule_app = Flask(__name__)

@schedule_app.route('/', methods=['GET', 'POST'])
def index():
    date = datetime.date.today()
#    date = datetime.date(date.year, date.month, 1)

    if str(request.form.get('day')) != 'None':
        # sch_day=datetime.datetime(date.year, date.month, int(request.form.get('day'))).date()
        # schedule_maker_if.cmd_remove_duty_by_day(sch_day)
        schedule_maker_if.cmd_remove_duty_by_day(int(request.form.get('day')))

    schedule_days=yaml.load(schedule_maker_if.cmd_show_schedule(int(date.strftime("%Y%m"))))
    schedule_month = process_month(date)

    result = render_template("index.html",
                            month = schedule_month['month'],
                            year = schedule_month['year'],
                            days = schedule_month['days'],
                            schedule_days = schedule_days)
    return result

@schedule_app.route('/useradd', methods=['GET', 'POST'])
def useradd():
    useradd_result=schedule_maker_if.cmd_add_user(request.form.get('user'))
    if useradd_result == 'ok':
        display_message='Пользователь {} успешно добавлен'.format(request.form.get('user'))
        schedule_maker_if.cmd_rebuild()
    else:
        display_message='Ошибка добавления пользователя'

    return render_template('user.html', message=display_message)

@schedule_app.route('/userdel', methods=['GET', 'POST'])
def userdel():
    useradd_result=schedule_maker_if.cmd_del_user(request.form.get('user'))
    if useradd_result == 'ok':
        display_message='Пользователь {} успешно удален'.format(request.form.get('user'))
        schedule_maker_if.cmd_rebuild()
    else:
        display_message='Ошибка удаления пользователя'

    return render_template('user.html', message=display_message)

@schedule_app.route('/duty', methods=['GET', 'POST'])
def duty():
    day = request.args.get('day')
    user = request.args.get('user')

    return render_template('dutyremove.html', day=day, user=user)

if __name__ == "__main__":
    setup_locale(sys.platform)
    schedule_app.run(host='0.0.0.0', port=int("8080"), debug=True)

