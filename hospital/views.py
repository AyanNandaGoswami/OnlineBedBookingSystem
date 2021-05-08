from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .models import *


class HospitalRegistrationView(View):
    template_name = 'hospital/hospital-registration.html'

    def get(self, request):
        states = State.objects.order_by('name').all()
        context = {
            'states': states 
        }
        return render(request, self.template_name, context)



