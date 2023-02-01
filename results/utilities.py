from results.models import User
from attendance.models import Codes
from datetime import timedelta
import datetime



#period number values:
p1 = 1
p2 = 2
p3 = 3
p4 = 4
p5 = 5
p6 = 6
p7 = 7
p8 = 8
p9 = 9
p10 = 10
p11 = 11
p12 = 12
p13 = 13
p14 = 14
p15 = 15
p16 = 16
p17 = 17
p18 = 18

#period choices for reports:
period_choices = [
    (p1, 'Period 1'),
    (p2, 'Period 2'),
    (p3, 'Period 3'),
    (p4, 'Period 4'),
    (p5, 'Period 5'),
    (p6, 'Period 6'),
    (p7, 'Period 7'),
    (p8, 'Period 8'),
    (p9, 'Period 9'),
    (p10, 'Period 10'),
    (p11, 'Period 11'),
    (p12, 'Period 12'),
    (p13, 'Period 13'),
    (p14, 'Year to Date'),
    (p15, 'Quarter 1'),
    (p16, 'Quarter 2'),
    (p17, 'Quarter 3'),
    (p18, 'Quarter 4'),
    ]

#enter results period choices:
period_result_options = [
        (p1, 'Period 1'),
    (p2, 'Period 2'),
    (p3, 'Period 3'),
    (p4, 'Period 4'),
    (p5, 'Period 5'),
    (p6, 'Period 6'),
    (p7, 'Period 7'),
    (p8, 'Period 8'),
    (p9, 'Period 9'),
    (p10, 'Period 10'),
    (p11, 'Period 11'),
    (p12, 'Period 12'),
    (p13, 'Period 13'),
]


def get_all_users():
    all_user_choices = []
    for x in User.objects.all():
        if x.is_active:
            if x.username == "mgangon":
                continue
            else:   
                all_user_choices.append((x.id, x.first_name+" "+x.last_name))
    return all_user_choices

def get_absence_types():
    absence_types = []
    for x in Codes.objects.all():
        absence_types.append((x.code_id, x.title))
    return absence_types

def get_start_date(x):
    return datetime.date.today() + timedelta(days=-x)

def get_current_quarter(x):
    if x >= 1 and x <=3:
        return 1
    elif x >=4 and x <= 6:
        return 2
    elif x >= 7 and x <=9:
        return 3
    elif x >=10 and x<=13:
        return 4

def set_current_streak(sos):
    current_strk = sos[0]
    if sos[1] == True:
        current_strk = current_strk + 1
    else:
        current_strk = 0
    if sos[2] == True:
        current_strk = current_strk + 1
    else:
        current_strk = 0
    if sos[3] == True:
        current_strk = current_strk + 1
    else:
        current_strk = 0
    if sos[4] == True:
        current_strk = current_strk + 1
    else:
        current_strk = 0
    if sos[5] == True:
        current_strk = current_strk + 1
    else:
        current_strk = 0
    if sos[6] == True:
        current_strk = current_strk + 1
    else:
        current_strk = 0
    return current_strk