from django.shortcuts import render
from .models import Class
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    classes = Class.objects.filter(
        date__gte='2020-10-01',
        date__lte='2020-10-31'
    )
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