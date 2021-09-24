from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


from . import serializers

from .models import Doctor, Client
from .permissions import IsProfileOwnerOrHospitalAdmin, IsProfileOwner


class ClientRegistrationAPIView(generics.CreateAPIView):
    """Registration of clients profiles"""
    permission_classes = (AllowAny,)
    serializer_class = serializers.ClientRegistrationSerializer


class DoctorRegistrationAPIView(generics.CreateAPIView):
    """Registration of doctors profiles"""
    permission_classes = (AllowAny,)
    serializer_class = serializers.DoctorRegistrationSerializer


class HospitalAdminRegistrationAPIView(generics.CreateAPIView):
    """Registration of hospital admins"""
    permission_classes = (AllowAny,)
    serializer_class = serializers.HospitalAdminRegistrationSerializer


class UserLogin(APIView):
    """Users login, by providing email and password"""
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve a doctor's profile"""
    serializer_class = serializers.DoctorProfileSerializer
    queryset = Doctor.objects.all()
    permission_classes = (IsProfileOwnerOrHospitalAdmin, )


class ClientProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """"Retrieve a clients profile"""
    serializer_class = serializers.ClientProfileSerializer
    queryset = Client.objects.all()
    permission_classes = (IsProfileOwner, )




