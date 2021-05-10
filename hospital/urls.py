from django.urls import path

from .views import *
from .api import *


app_name = 'hospital'


urlpatterns = [
    # path for view
    path('registration', HospitalRegistrationView.as_view(), name='registration'),
    path('authority-dashboard', HospitalDashboardView.as_view(), name='dashboard'),

    # path for api
    path('register-new-hospital/', CreateHospital.as_view(), name='register_new_hospital'),
    path('get-patients/<slug:status>', PatientListView.as_view(), name='get_patients'),
]

