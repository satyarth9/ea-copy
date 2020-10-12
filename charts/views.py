from django.shortcuts import render
from reports.models import Class
from json import dumps


def home(request):
    classes = Class.objects.filter(
        date__gte="2020-10-1",
        date__lte="2020-10-31"
    )
    day_totals = get_day_totals(classes)
    charts_date, charts_day_totals, charts_cum_totals = get_for_chart(day_totals)
    context = {
        "day_totals": day_totals,
        "charts_date": charts_date,
        "charts_day_totals" : charts_day_totals,
        "charts_cum_totals" : charts_cum_totals
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
        dates.append(int(key.strftime("%d")))
        d_t.append(day_totals[key][0])
        d_c.append(day_totals[key][1])

    return dates, d_t, d_c