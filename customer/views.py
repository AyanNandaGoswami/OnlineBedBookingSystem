from django.shortcuts import render, redirect
from django.views import View

from hospital.models import Hospital


def logged_in(request):
    user = request.user

    if user.is_authenticated == True and user.admin == False and user.is_customer == True and user.is_authority == False:
        return True
    else:
        return False


class CustomerLoginView(View):
    template_name = 'customer/customer-login-registration.html'

    def get(self, request):
        if logged_in(request):
            return redirect('customer:customer_dashboard')
        else:    
            return render(request, self.template_name, {'title': 'Customer Sign in'})


class CustomerRegistrationView(View):
    template_name = 'customer/customer-login-registration.html'

    def get(self, request):
        return render(request, self.template_name, {'class': 'right-panel-active', 'title': 'Customer Sign up'})


class CustomerDashboardView(View):
    template_name = 'customer/customer-dashboard.html'

    def get(self, request):
        if logged_in(request):
            hospitals = Hospital.objects.order_by('name').all()
            return render(request, self.template_name, {'hospitals': hospitals})
        else:
            return redirect('customer:customer_login')





