import sys
from flask import Flask, render_template, request
import datetime
from dateutil.relativedelta import relativedelta
from calendar import Calendar
# import yaml
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

    if str(request.form.get('month_cur')) != 'None':
        date = datetime.date(year=int(request.form.get('month_cur'))//100, month=int(request.form.get('month_cur'))%100, day=1)
    else: 
        date = datetime.date.today()
        #date = datetime.date(date.year, 2, 1)

    if str(request.form.get('month_next')) != 'None':
        date = date + relativedelta(months=1)
    elif str(request.form.get('month_prev')) != 'None':
        date = date - relativedelta(months=1)
        

    if str(request.form.get('month_schedule')) != 'None':
        print(request.form.get('month_schedule'))
        schedule_maker_if.cmd_make_schedule(int(request.form.get('month_schedule')))

    if str(request.form.get('day')) != 'None':
        # sch_day=datetime.datetime(date.year, date.month, int(request.form.get('day'))).date()
        # schedule_maker_if.cmd_remove_duty_by_day(sch_day)
        schedule_maker_if.cmd_remove_duty_by_day(int(request.form.get('day')), int(date.strftime("%Y%m")))

    if str(request.form.get('setday')) == 'holyday':
        # sch_day=datetime.datetime(date.year, date.month, int(request.form.get('day'))).date()
        # schedule_maker_if.cmd_remove_duty_by_day(sch_day)
        schedule_maker_if.cmd_set_holyday(int(request.form.get('day')), int(date.strftime("%Y%m")))
    elif str(request.form.get('setday')) == 'workday':
        schedule_maker_if.cmd_set_weekday(int(request.form.get('day')), int(date.strftime("%Y%m")))

    # schedule_days=yaml.load(schedule_maker_if.cmd_show_schedule(int(date.strftime("%Y%m"))))
    schedule_days = schedule_maker_if.cmd_show_schedule(int(date.strftime("%Y%m")))
    schedule_month = process_month(date)
    schedule_users = schedule_maker_if.cmd_show_user()

    result = render_template("index.html",
                            month = schedule_month['month'],
                            month_digit=int(date.strftime("%Y%m")),
                            year = schedule_month['year'],
                            days = schedule_month['days'],
                            schedule_days = schedule_days,
                            schedule_users = schedule_users)
    return result

@schedule_app.route('/useradd', methods=['GET', 'POST'])
def useradd():
    useradd_result=schedule_maker_if.cmd_add_user(request.form.get('user'))
    month_digit=request.form.get('month_cur')
    if useradd_result == 'ok':
        display_message='Пользователь {} успешно добавлен'.format(request.form.get('user'))
        schedule=schedule_maker_if.cmd_make_schedule(int(request.form.get('month_cur')))
        # print(type(request.args.get('month')))
        schedule_maker_if.cmd_rebuild(int(request.form.get('month_cur')))
    else:
        display_message='Ошибка добавления пользователя'

    return render_template('user.html', message=display_message, month_digit=month_digit)

@schedule_app.route('/userdel', methods=['GET', 'POST'])
def userdel():
    useradd_result=schedule_maker_if.cmd_del_user(request.form.get('user'))
    month_digit=request.form.get('month_cur')
    if useradd_result == 'ok':
        display_message='Пользователь {} успешно удален'.format(request.form.get('user'))
        print(request.args.get('month_cur'))
        schedule_maker_if.cmd_rebuild(int(request.form.get('month_cur')))
    else:
        display_message='Ошибка удаления пользователя'

    return render_template('user.html', message=display_message, month_digit=month_digit)

@schedule_app.route('/duty', methods=['GET', 'POST'])
def duty():
    day = request.args.get('day')
    month_digit= request.args.get('month')
    user = request.args.get('user')

    return render_template('dutyremove.html', day=day, month_digit=month_digit, user=user)

@schedule_app.route('/day', methods=['GET', 'POST'])
def holyday():
    day = request.args.get('day')
    month_digit= request.args.get('month')

    return render_template('day.html', day=day, month_digit=month_digit)

if __name__ == "__main__":
    setup_locale(sys.platform)
    schedule_app.run(host='0.0.0.0', port=8080, debug=True)

