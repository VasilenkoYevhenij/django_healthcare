from django.urls import path
from . import views


urlpatterns = [
    # Hospitals

    path('hospitals/', views.HospitalListAPIView.as_view()),
    path('hospitals/<int:pk>/', views.HospitalDetailAPIView.as_view()),
    path('hospitals/<str:url>/', views.HospitalsByServicesListAPIView.as_view(), name='hospital-services'),
    path('hospitals/<int:pk>/like/', views.HospitalLikeCreateAPIView.as_view()),
    path('hospitals/<int:pk>/like/delete/', views.HospitalLikeDeleteAPIView.as_view()),
    path('hospitals/<int:pk>/review/create/', views.HospitalReviewCreateAPIView.as_view()),

    # Doctors
    path('doctors/<str:url>/', views.DoctorsBySpecializationsListAPIView.as_view(), name='specializations'),
    path('schedule/', views.ScheduleListCreateAPIView.as_view()),
    path('booking/', views.BookingCreateAPIView.as_view()),
    path('booking/list/', views.BookingListAPIView.as_view()),
    path('booking/<int:pk>/', views.BookingDestroyAPIView.as_view()),
    # path('schedule/delete/', views.ScheduleDestroyAPIView.as_view()),


    path('hospitals/<int:pk>/doctors/', views.DoctorsByHospitalsListAPIView.as_view()),
    path('doctors/<str:url>/', views.DoctorsBySpecializationsListAPIView.as_view(), name='specializations'),
    path('search/<str:q>/', views.SearchCombinedAPIView.as_view()),

    path('doctor/<int:pk>/visits/', views.VisitListAPIView.as_view()),
    path('doctor/visits/<int:pk>/', views.VisitDestroyAPIView.as_view(), name='visit-detail'),
    path('doctor/<int:pk>/feedback/create/', views.FeedbackCreateAPIView.as_view()),
    path('doctor/<int:pk>/like/', views.DoctorLikeCreateAPIView.as_view()),
    path('doctor/<int:pk>/like/delete/', views.DoctorLikeDeleteAPIView.as_view()),


    path('specializations/', views.SpecializationListAPIView.as_view()),
    path('services/', views.ServiceListAPIView.as_view())
]
