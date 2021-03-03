from django.shortcuts import render
from home.models import Student
from reports.models import Class
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


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
    ).order_by('date', 'start_time')
    students = Student.objects
    context = {
        'students': students,
        'class_data': class_data
    }
    return render(request, 'invoices/invoice_home.html', context)


def generate_invoice(request):
    left_margin = 100
    top_margin = 800
    cursor_x = left_margin
    cursor_y = top_margin
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
#    p.drawImage("https://www.smallworldfs.com/filemanager/userfiles/news/smallnew2.png", left_margin, top_margin)
    p.setAuthor("Asymptote Education")
    p.setFont("Helvetica", 20)
    p.setFillColorRGB(0,0,1)
    p.setStrokeColorRGB(0,0,0.5)
    p.drawString(cursor_x + 20, cursor_y, "Class Details:")
    cursor_y -= 10
    p.rect(cursor_x, cursor_y, 300, 40, fill=0, stroke=1)
    cursor_y -= 2
    p.line(cursor_x, cursor_y, cursor_x + 300, cursor_y)
    p.line(cursor_x, cursor_y, cursor_x, cursor_y - len(class_data) * 15)
    cursor_x += 5
    p.setFont("Helvetica", 12)
    for i in range(len(class_data)):
        cursor_y -= 15
        p.drawString(cursor_x, cursor_y, f"{class_data[i].date} {class_data[i].payout}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{invoice_particulars[0]} - Dec20")


@login_required
def generate_invoice_legacy(request):
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