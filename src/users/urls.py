from django.urls import path
from .views import (
    UserLogin, DoctorRegistrationAPIView, ClientRegistrationAPIView,
    HospitalAdminRegistrationAPIView, DoctorProfileAPIView, ClientProfileAPIView
)

urlpatterns = [
    path('client/register/', ClientRegistrationAPIView.as_view(), name='client-register'),
    path('doctor/register/', DoctorRegistrationAPIView.as_view(), name='doctor-register'),
    path('doctor/profile/<int:pk>/', DoctorProfileAPIView.as_view()),
    path('profile/<int:pk>/', ClientProfileAPIView.as_view()),
    path('hospital-admin/register/', HospitalAdminRegistrationAPIView.as_view(), name='hospital-admin-register'),
    path('login/', UserLogin.as_view())
]
