from django.shortcuts import render
from home.models import Student
from reports.models import Class
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    students = Student.objects
    context = {
        'students': students
    }
    return render(request, 'invoices/invoice_home.html', context)


invoice_particulars = []
class_data = None

def student_invoice(request):
    global invoice_particulars, class_data
    if request.method == "POST":
        invoice_particulars.clear()
        class_data = None
        student = request.POST["invoice_student"]
        start_date = request.POST["invoice_start_date"]
        end_date = request.POST["invoice_end_date"]
        invoice_particulars.extend((student, start_date, end_date))
    class_data = Class.objects.filter(
        student= student,
        date__gte=start_date,
        date__lte=end_date
    )
    students = Student.objects
    context = {
        'students': students,
        'class_data': class_data
    }
    return render(request, 'invoices/invoice_home.html', context)


def generate_invoice(request):
    global class_data
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = f'attachment; filename={invoice_particulars[0]}_' \
                                      f'{invoice_particulars[1]}_' \
                                      f'{invoice_particulars[2]}.csv"'
    writer = csv.writer(response)
    writer.writerow(["Name", "Date", "Start Time", "End Time", "Subject", "Topic", "Remarks", "Payout"])
    no_of_classes = 0
    total_hours = 0
    total_payout = 0
    for data in class_data:
        no_of_classes += 1
        total_hours += data.duration
        total_payout += data.payout
        writer.writerow([data.student, data.date, data.start_time, data.end_time, data.subject, data.topic, data.remarks, data.payout])

    writer.writerow(["","number of classes", no_of_classes])
    writer.writerow(["","total hours", total_hours])
    writer.writerow(["","total payout", total_payout])
    return response