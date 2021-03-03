from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def all_links(request):
    return render(request, 'links/all_links.html')
