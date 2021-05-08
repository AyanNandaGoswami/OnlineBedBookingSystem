from django.urls import path

from .views import *
from .api import *


app_name = 'hospital'


urlpatterns = [
    # path for view
    path('registration', HospitalRegistrationView.as_view(), name='registration'),

    # path for api
    path('register-new-hospital/', CreateHospital.as_view(), name='register_new_hospital')
]

