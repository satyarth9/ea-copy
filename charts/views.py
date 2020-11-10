from django.shortcuts import render
from reports.models import Class
from datetime import datetime
import reports.views as rviews


def home(request, tab_id):
    if tab_id in (1,2):
        start_date, end_date = rviews.get_dates(tab_id)
    else:
        start_date, end_date = request.POST["modal_start_date"], request.POST["modal_end_date"]
    classes = Class.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    ).order_by("date", "start_time")
    day_totals = get_day_totals(classes)
    charts_date, charts_day_totals, charts_cum_totals = get_for_chart(day_totals)
    charts_students, charts_stu_totals = get_student_wise(classes)
    context = {
        "day_totals": day_totals,
        "charts_date": charts_date,
        "charts_day_totals" : charts_day_totals,
        "charts_cum_totals" : charts_cum_totals,
        "students": charts_students,
        "chart_student_totals" : charts_stu_totals
    }
    return render(request, 'charts/home.html', context)


def get_day_totals(classes):
    d_wise = {}
    for c in classes:
        if c.date in d_wise:
            d_wise[c.date][0] += c.payout
        else:
            d_wise[c.date] = []
            d_wise[c.date].append(c.payout)
    cum = 0
    for day in d_wise:
        cum += d_wise[day][0]
        d_wise[day].append(cum)
    return d_wise


def get_for_chart(day_totals):
    dates = []
    d_t = []
    d_c = []
    for key in day_totals:
        dates.append(f"{key.strftime('%d')} {key.strftime('%b')}")
        d_t.append(day_totals[key][0])
        d_c.append(day_totals[key][1])

    return dates, d_t, d_c


def get_student_wise(classes):
    s_wise = {}
    for c in classes:
        if c.student in s_wise:
            s_wise[c.student] += c.payout
        else:
            s_wise[c.student] = c.payout
    s_wise = {k: v for k, v in sorted(s_wise.items(), key=lambda item: item[1], reverse=True)}
    return list(s_wise.keys()), list(s_wise.values())