from django.shortcuts import render, redirect
from django.views import View

from .models import *


def logged_in(request):
    user = request.user

    if user.is_authenticated == True and user.admin == False and user.is_customer == False and user.is_authority == True:
        return True
    else:
        return False


class HospitalRegistrationView(View):
    template_name = 'hospital/hospital-registration.html'

    def get(self, request):
        states = State.objects.order_by('name').all()
        context = {
            'states': states 
        }
        return render(request, self.template_name, context)


class HospitalDashboardView(View):
    template_name = 'hospital/hospital-dashboard.html'
    
    def get(self, request):
        if logged_in(request):
            return render(request, self.template_name)
        else:
            return redirect('hospital:registration')





