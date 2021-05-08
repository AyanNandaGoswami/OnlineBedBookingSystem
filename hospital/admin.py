from django.contrib import admin

from .models import *


class StateAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 20
admin.site.register(State, StateAdmin)


class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'hospital_type', 'help_line', 'updated_at', 'created_at']
    list_filter = ['name', 'hospital_type']
admin.site.register(Hospital, HospitalAdmin)




