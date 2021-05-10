from django.urls import path

from .views import *
from .api import *


app_name = 'customer'


urlpatterns = [
    # path for view
    path('login', CustomerLoginView.as_view(), name='customer_login'),
    path('registration', CustomerRegistrationView.as_view(), name='customer_registration'),
    path('dashboard', CustomerDashboardView.as_view(), name='customer_dashboard'),

    # path for api
    path('create-new-customer/', CustomerRegisterAPI.as_view(), name='create_new_customer'),
    path('customer-logout', CustomerLogoutAPIView.as_view(), name='customer_logout'),
]

