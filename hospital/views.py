from django.shortcuts import render, redirect
from django.views import View

from .models import *
from bookpatient.models import Notification


def logged_in(request):
    user = request.user

    if user.is_authenticated == True and user.admin == False and user.is_customer == False and user.is_authority == True:
        return True
    else:
        return False


class HospitalRegistrationView(View):
    template_name = 'hospital/hospital-registration.html'

    def get(self, request):
        return render(request, self.template_name)


class HospitalLoginView(View):
    template_name = 'hospital/hospital-authority-login.html'

    def get(self, request):
        if logged_in(request):
            return redirect('hospital:dashboard')
        else:
            return render(request, self.template_name)


class HospitalDashboardView(View):
    template_name = 'hospital/hospital-dashboard.html'
    
    def get(self, request):
        if logged_in(request):
            hospitals = Hospital.objects.order_by('name').all()
            notifications = Notification.objects.order_by('-timestamp').all()
            return render(request, self.template_name, {'hospitals': hospitals, 'notifications': notifications})
        else:
            return redirect('hospital:login')





