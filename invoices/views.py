from django.shortcuts import render
from home.models import Student
from reports.models import Class

def home(request):
    students = Student.objects
    context = {
        'students': students
    }
    return render(request, 'invoices/invoice_home.html', context)


def student_invoice(request):
    if request.method == "POST":
        student = request.POST["invoice_student"]
        start_date = request.POST["invoice_start_date"]
        end_date = request.POST["invoice_end_date"]
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