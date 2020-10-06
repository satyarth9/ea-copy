from django.shortcuts import render

def home(request):
    return render(request, 'invoices/invoice_home.html')