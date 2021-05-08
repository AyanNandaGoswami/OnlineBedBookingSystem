from django.urls import path

from .views import *

app_name = 'hospital'

urlpatterns = [
    path('registration', HospitalRegistrationView.as_view(), name='registration'),
]

