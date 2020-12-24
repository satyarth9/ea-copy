from django.shortcuts import render

# Create your views here.

def all_links(request):
    return render(request, 'links/all_links.html')
