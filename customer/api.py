from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from userapp.serializers import AccountRegisterSerializer


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

