from django.shortcuts import render
from .models import Payment


def home(request):
    payments = Payment.objects.all()
    payments_json = get_students(payments)
    context = {
        'payments_json' : payments_json
    }
    return render(request, 'payments/payments_home.html', context)


def get_students(payments):
    json = {}
    for payment in payments:
        if payment.student_name in json:
            json[payment.student_name].append([
                payment.span,
                payment.amount,
                payment.received_datetime,
                payment.mode
            ])
        else:
            json[payment.student_name] = [[
                payment.span,
                payment.amount,
                payment.received_datetime,
                payment.mode
            ]]
    return json