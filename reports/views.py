from django.shortcuts import render
from .models import Class
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta


@login_required
def dashboard(request, tab_id):
    if tab_id in (1,2):
        start_date, end_date = get_dates(tab_id)
    else:
        start_date, end_date = request.POST["modal_start_date"], request.POST["modal_end_date"]
    classes = Class.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date', 'start_time')
    total, hours, hourly_average = get_totals(classes)
    student_wise = get_student_wise(classes)
    subject_wise = get_subject_wise(classes)
    return render(request, 'reports/dashboard.html', {'classes': classes,
                                                      'total': total,
                                                      'hours': hours,
                                                      'hourly_average' : hourly_average,
                                                      'student_wise': student_wise,
                                                      'subject_wise' : subject_wise})


def get_totals(classes):
    total = 0
    hours = 0
    for c in classes:
        total += c.payout
        hours += c.duration
    return total, hours, int(total/hours)


def get_student_wise(classes):
    s_wise = {}
    for c in classes:
        if c.student in s_wise:
            s_wise[c.student][0] += c.payout
            s_wise[c.student][1] += c.duration
        else:
            s_wise[c.student] = []
            s_wise[c.student].append(c.payout)
            s_wise[c.student].append(c.duration)
    s_wise = {k: v for k, v in sorted(s_wise.items(), key=lambda item: item[1], reverse=True)}
    return s_wise


def get_subject_wise(classes):
    s_wise = {}
    for c in classes:
        if c.subject in s_wise:
            s_wise[c.subject][0] += c.payout
            s_wise[c.subject][1] += c.duration
        else:
            s_wise[c.subject] = []
            s_wise[c.subject].append(c.payout)
            s_wise[c.subject].append(c.duration)
    s_wise = {k: v for k, v in sorted(s_wise.items(), key=lambda item: item[1], reverse=True)}
    return s_wise


def get_dates(tab_id):
    if tab_id == 1:
        start_date = datetime.now().replace(day=1)
        month = int(datetime.now().strftime("%m"))
        if month in [1, 3, 5, 7, 8, 10, 12]:
            last_date = 31
        elif month in [4, 6, 9, 11]:
            last_date = 30
        else:
            if datetime.now().year % 4 == 0:  # not checking for century years
                last_date = 29
            else:
                last_date = 28
        end_date = datetime.now().replace(day=last_date)
        return start_date, end_date
    if tab_id == 2:
        today = date.today()
        first = today.replace(day=1)
        prev_month_last = first - timedelta(days=1)
        prev_month_first = prev_month_last.replace(day=1)
        return prev_month_first, prev_month_last
