from django.shortcuts import render
from .models import Student, Subject
from reports.models import Class


def landing(request):
    students = Student.objects
    subjects = Subject.objects
    return render(request, 'home/landing.html', {'students': students, 'subjects' : subjects})


def add_class(request):
    if request.method == "POST":
        session = Class()
        session.student = request.POST['student_form']
        session.date = request.POST['date']
        session.start_time = request.POST['start_time']
        session.end_time = request.POST['end_time']
        session.subject = request.POST['subject']
        session.topic = request.POST['topic']
        session.homework = request.POST['homework']
        session.brought_over = request.POST['brought_over']
        session.remarks = request.POST['remarks']
        session.duration = request.POST['duration']
        session.payout = request.POST['payout']
        session.save()
    students = Student.objects
    subjects = Subject.objects
    return render(request, 'home/landing.html', {'students': students, 'subjects': subjects})
