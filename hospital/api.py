from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import *
from .serializers import *


class CreateHospital(GenericAPIView):
    
    def post(self, request):
        data = request.data

        context = {
            'username': data['username'],
            'password': data['password']
        }

        user_serializer = UserSerializer(data=context)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            return Response(user_serializer.errors)

        user = User.objects.get(username=user_serializer.data['username'])  # get user obj

        state = State.objects.get(slug=data['state'])   # get state object

        data._mutable = True
        data['state'] = state.id    # change state value to a objcet_id
        data['user'] = user.id      # change user value to a user_object_id
        request.data._mutable = False

        serializer = HospitalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'user_deatils': serializer.data, 'login': True})
        return Response(serializer.errors)
  
