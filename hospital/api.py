from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, redirect

from .models import *
from customer.models import *
from customer.serializers import *
from .serializers import *
from userapp.serializers import AccountRegisterSerializer


class CreateHospital(GenericAPIView):
    
    def post(self, request):
        data = request.data

        context = {
            'username': data['username'],
            'password': data['password'],
            'email': data['email'],
            'is_authority': True
        }

        user_serializer = AccountRegisterSerializer(data=context)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            return Response(user_serializer.errors)

        user = Account.objects.get(username=user_serializer.data['username'])  # get user obj

        data._mutable = True
        data['user'] = user.pk      # change user value to a user_object_id

        serializer = HospitalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return Response({'user_deatils': serializer.data, 'login': True})
        return Response(serializer.errors)
  

class HospitalAuthorityLoginAPI(GenericAPIView):

    def post(self, request):
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            login(request, user)
            return Response({'login': True})
        return Response({'error': 'Incorrect login credentials.', 'login': False})


class HospitalAuthorityLogoutAPI(GenericAPIView):

    def get(self, request):
        user = request.user
        if user:
            logout(request)
        return redirect('hospital:login')


class PatientListView(GenericAPIView):
    serializer_class = PatientSerializer

    def get(self, request, status):
        user = request.user
        hospital = None
        try:
            hospital = Hospital.objects.get(user=user)
        except:
            pass

        if hospital != None:
            word_bed = hospital.word_bed
            icu_bed = hospital.icu_bed
            if status == 'All':
                patient_queryset = Patient.objects.order_by('-update_at').filter(Q(hospital=hospital.pk))
                patient_serialized_data = self.serializer_class(patient_queryset, many=True)
                return Response({'patients': patient_serialized_data.data, 'status': status, 'word_bed': word_bed, 'icu_bed': icu_bed})
            else:
                patient_queryset = Patient.objects.order_by('-update_at').filter(Q(hospital=hospital.pk) & Q(status__iexact=status))
                patient_serialized_data = self.serializer_class(patient_queryset, many=True)
                return Response({'patients': patient_serialized_data.data, 'status': status, 'word_bed': word_bed, 'icu_bed': icu_bed})
        else:
            if status == 'All':
                patient_queryset = Patient.objects.order_by('-update_at').filter(Q(reference_user=user.pk))
                patient_serialized_data = self.serializer_class(patient_queryset, many=True)
                return Response({'patients': patient_serialized_data.data, 'status': status})
            else:
                patient_queryset = Patient.objects.order_by('-update_at').filter(Q(reference_user=user.pk) & Q(status__iexact=status))
                patient_serialized_data = self.serializer_class(patient_queryset, many=True)
                return Response({'patients': patient_serialized_data.data, 'status': status})


class UpdateBedAPI(GenericAPIView):
    def post(self, request):
        data = request.data
        hospital_obj = Hospital.objects.get(user=request.user)

        if data['bed_type'] == 'word_bed':
            hospital_obj.word_bed = data['bed']
            hospital_obj.save()
        elif data['bed_type'] == 'icu_bed':
            hospital_obj.icu_bed = data['bed']
            hospital_obj.save()
        return Response({'word_bed': hospital_obj.word_bed, 'icu_bed': hospital_obj.icu_bed})


class PatientDetailView(GenericAPIView):
    template_name = 'customer/patient-view.html'
    page_not_found = 'page-not-found.html'

    def get(self, request, slug):
        try:
            patient_obj = Patient.objects.get(slug=slug)
            patient_serialized_data = PatientSerializer(patient_obj, many=False)
            return render(request, self.template_name, {'patient': patient_serialized_data.data})
        except:
            return render(request, self.page_not_found, {'info': 'Patient not found.'})





