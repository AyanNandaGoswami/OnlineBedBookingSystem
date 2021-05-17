from customer.models import Patient
from hospital.models import Hospital
from rest_framework.generics import GenericAPIView
from rest_framework import serializers, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from userapp.serializers import AccountRegisterSerializer
from .serializers import PatientSerializer
from bookpatient.models import BookingRequest, TempPatientDetails, Notification, Activity


class CustomerRegisterAPI(GenericAPIView):
    serializer_class = AccountRegisterSerializer

    def post(self, request):
        data = request.data
        data._mutable = True
        data['is_customer'] = True

        user_serializer = self.serializer_class(data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return Response({'user_deatils': user_serializer.data, 'login': True})
        else:
            return Response(user_serializer.errors)


class CustomerLogoutAPIView(GenericAPIView):

    def get(self, request):
        user = request.user
        if user:
            logout(request)
        return redirect('customer:customer_login')


# make it only for hospital authority(due)
class AddPatientAPI(GenericAPIView):

    def post(self, request):
        data = request.data
        user = request.user
        try:
            hospital = Hospital.objects.get(user=user)
            patient = Patient.objects.create(reference_user=user, hospital=hospital, name=data['name'], gender=data['gender'], p_mobile=data['p_mobile'], s_mobile=data['s_mobile'], adhar=data['adhar'], dob=data['dob'])
            if patient:
                text = f'You ({user.username}) added a new patient {data["name"]}.'
                Activity.objects.create(user=user, text=text)
                return Response({'added': True})
            return Response({'added': False})
        except:
            hospital = Hospital.objects.get(slug=data['hospital'])  
            patient = Patient.objects.create(reference_user=user, hospital=hospital, name=data['name'], gender=data['gender'], p_mobile=data['p_mobile'], s_mobile=data['s_mobile'], adhar=data['adhar'], dob=data['dob'])
            if patient:
                return Response({'added': True})
            return Response({'added': False})


class UpdatePatientDetailAPI(GenericAPIView):

    def post(self, request):
        data = request.data
        patient_through_adhar = None

        patient = Patient.objects.get(slug=data['slug'])

        try:
            patient_through_adhar = Patient.objects.get(adhar=data['adhar'])
        except:
            pass

        if patient_through_adhar != None:
            if patient_through_adhar.slug != patient.slug:
                return Response({'update': False})
        
        patient.name = request.POST.get('name', patient.name)
        patient.gender = request.POST.get('gender', patient.gender)
        patient.p_mobile = request.POST.get('p_mobile', patient.p_mobile)
        patient.s_mobile = request.POST.get('s_mobile', patient.s_mobile)
        patient.adhar = request.POST.get('adhar', patient.adhar)
        patient.dob = request.POST.get('dob', patient.dob)
        patient.status = request.POST.get('status', patient.status)
        patient.save()

        patient_serialized_data = PatientSerializer(patient)
        return Response({'patient': patient_serialized_data.data, 'update': True})        


class TempAddPatientAPI(GenericAPIView):

    def create_noticication_(self, hospital_id, user, booking_obj):
        notification_body = f'{user.username} requested for a ICU bed.'
        notification = Notification.objects.create(hospital_id=hospital_id, notification_body=notification_body, booking_request=booking_obj)

    def update_booking_obj(self, adhar, hospital):
        booking_obj = BookingRequest.objects.get(adhar=adhar)   # get booking_request obj
        booking_obj.to_hospital.add(hospital)   # add hospital to bookking_request obj
        return booking_obj

    def post(self, request):
        data = request.data
        user = request.user
        hospital = Hospital.objects.get(slug=data['hospital'])
        temp_patient = None

        try:
            temp_patient = TempPatientDetails.objects.get(adhar=data['adhar'])
        except:
            pass
        
        if temp_patient != None:
            temp_patient.hospital.add(hospital)
            booking_obj = self.update_booking_obj(data['adhar'], hospital)
            self.create_noticication_(hospital.hospital_id, user, booking_obj)   # create new notification
        else:
            temp_patient = TempPatientDetails.objects.create(reference_user=user, name=data['name'], gender=data['gender'], p_mobile=data['p_mobile'], s_mobile=data['s_mobile'], adhar=data['adhar'], dob=data['dob'])
            temp_patient.hospital.add(hospital) # add hospital to temp_patient obj
            booking_obj =self.update_booking_obj(data['adhar'], hospital)
            self.create_noticication_(hospital.hospital_id, user, booking_obj)   # create new notification

        if temp_patient:
            return Response({'added': True, 'hospital_id': hospital.hospital_id})
        return Response({'added': False})
