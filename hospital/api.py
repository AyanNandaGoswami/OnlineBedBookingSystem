from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.db.models import Q

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

        state = State.objects.get(slug=data['state'])   # get state object

        data._mutable = True
        data['state'] = state.id    # change state value to a objcet_id
        data['user'] = user.pk      # change user value to a user_object_id
        request.data._mutable = False

        serializer = HospitalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return Response({'user_deatils': serializer.data, 'login': True})
        return Response(serializer.errors)
  

class PatientListView(GenericAPIView):
    serializer_class = PatientSerializer

    def get_patients(self, user, status):
        if status == 'All':
            queryset = Patient.objects.order_by('-update_at').filter(Q(reference_user=user.pk))
            return queryset
        else:
            queryset = Patient.objects.order_by('-update_at').filter(Q(reference_user=user.pk) & Q(status__iexact=status))
            return queryset

    def get(self, request, status):
        user = request.user
        patient_queryset = self.get_patients(user, status)
        patient_serialized_data = self.serializer_class(patient_queryset, many=True)
        return Response({'patients': patient_serialized_data.data, 'status': status})

