"""earnings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import home.views
import reports.views
import invoices.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home.views.landing, name="landing"),
    path('reports/', reports.views.dashboard, name="dashboard"),
    path('invoices/', invoices.views.home, name="invoices_home"),
    path('add_class/', home.views.add_class, name="add_class"),
    path('invoice/student/', invoices.views.student_invoice,
         name="student_invoice"),

]
