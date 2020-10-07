from django.shortcuts import render
from .models import Class
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    classes = Class.objects.filter(
        date__gte='2020-10-01'
    )
    total, hours = get_totals(classes)
    student_wise = get_student_wise(classes)
    subject_wise = get_subject_wise(classes)
    return render(request, 'reports/dashboard.html', {'classes': classes,
                                                      'total': total,
                                                      'hours': hours,
                                                      'student_wise': student_wise,
                                                      'subject_wise' : subject_wise})


def get_totals(classes):
    total = 0
    hours = 0
    for c in classes:
        total += c.payout
        hours += c.duration
    return total, hours


def get_student_wise(classes):
    s_wise = {}
    for c in classes:
        if c.student in s_wise:
            s_wise[c.student] += c.payout
        else:
            s_wise[c.student] = c.payout
    s_wise = {k: v for k, v in sorted(s_wise.items(), key=lambda item: item[1], reverse=True)}
    return s_wise


def get_subject_wise(classes):
    s_wise = {}
    for c in classes:
        if c.subject in s_wise:
            s_wise[c.subject] += c.payout
        else:
            s_wise[c.subject] = c.payout
    s_wise = {k: v for k, v in sorted(s_wise.items(), key=lambda item: item[1], reverse=True)}
    return s_wise