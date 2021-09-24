from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers
from .models import Hospital, Specialization, Service, Schedule, Visit, Booking, HospitalLike, Review, Feedback, \
    DoctorLike
from .permissions import IsHospitalAdminOrReadOnly, IsVisitOwner, IsBookingAdmin
from .schedule_generator import schedule_choose
from users.models import Doctor


class HospitalListAPIView(generics.ListAPIView):
    """List of all hospitals"""
    serializer_class = serializers.HospitalListSerializer
    queryset = Hospital.objects.all()
    permission_classes = (AllowAny, )


class HospitalDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve all information about hospital"""
    serializer_class = serializers.HospitalDetailSerializer
    queryset = Hospital.objects.all()
    permission_classes = (IsHospitalAdminOrReadOnly, )


class SpecializationListAPIView(generics.ListAPIView):
    """View for list of doctor's Specializations"""
    serializer_class = serializers.SpecializationListSerializer
    queryset = Specialization.objects.all()
    permission_classes = (AllowAny,)


class ServiceListAPIView(generics.ListAPIView):
    """View for list of hospital's Services"""
    serializer_class = serializers.ServiceListSerializer
    queryset = Service.objects.all()
    permission_classes = (AllowAny,)


class HospitalsByServicesListAPIView(generics.ListAPIView):
    """List of hospitals by certain services"""

    serializer_class = serializers.HospitalListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        service = get_object_or_404(Service, url=self.kwargs.get('url'))
        return Hospital.objects.filter(services=service).order_by('-hospital_likes_amount')


class DoctorsBySpecializationsListAPIView(generics.ListAPIView):
    """List of doctors by certain specializations"""

    serializer_class = serializers.DoctorListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        specialization = get_object_or_404(Specialization, url=self.kwargs.get('url'))
        return Doctor.objects.filter(specialization=specialization).order_by('-doctor_likes_amount')


class DoctorsByHospitalsListAPIView(generics.ListAPIView):
    """List of doctors by certain hospitals"""

    serializer_class = serializers.DoctorListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        hospital = get_object_or_404(Hospital, pk=self.kwargs.get('pk'))
        return Doctor.objects.filter(hospital=hospital).order_by('-doctor_likes_amount')


class SearchCombinedAPIView(generics.ListAPIView):
    """Search filter, by contains in doctors, hospitals, specializations and services"""

    serializer_class_doctors = serializers.DoctorListSerializer
    serializer_class_hospitals = serializers.HospitalListSerializer
    serializer_class_specializations = serializers.SpecializationListSerializer
    serializer_class_services = serializers.ServiceListSerializer
    permission_classes = (AllowAny,)

    def get_queryset_doctors(self):
        return Doctor.objects.filter(last_name__contains=self.kwargs.get('q'))

    def get_queryset_hospitals(self):
        return Hospital.objects.filter(title__contains=self.kwargs.get('q'))

    def get_queryset_specializations(self):
        return Specialization.objects.filter(title__contains=self.kwargs.get('q'))

    def get_queryset_services(self):
        return Service.objects.filter(title__contains=self.kwargs.get('q'))

    def list(self, request, *args, **kwargs):
        doctors = self.serializer_class_doctors(self.get_queryset_doctors(), many=True)
        hospitals = self.serializer_class_hospitals(self.get_queryset_hospitals(), many=True)
        specializations = self.serializer_class_specializations(self.get_queryset_specializations(), many=True)
        services = self.serializer_class_services(self.get_queryset_services(), many=True)

        return Response({
            "Doctors": doctors.data,
            "Hospitals": hospitals.data,
            "Specializations": specializations.data,
            "Services": services.data
        })


class ScheduleListCreateAPIView(generics.ListCreateAPIView):
    """Creating schedule for each doctor"""
    serializer_class = serializers.ScheduleSerializer

    def get_queryset(self):
        return Schedule.objects.filter(doctor=self.request.user.user_doctor)

    def perform_create(self, serializer):
        return schedule_choose(serializer, self.request.user.user_doctor)


class VisitListAPIView(generics.ListAPIView):
    """List of able visits"""
    serializer_class = serializers.VisitSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Visit.objects.filter(doctor=self.kwargs.get('pk')).order_by('date')[:25]


class VisitDestroyAPIView(generics.RetrieveDestroyAPIView):
    """View for destroying or retrieving a visit"""
    serializer_class = serializers.VisitSerializer
    queryset = Visit.objects.all()
    permission_classes = (IsVisitOwner, )


class BookingCreateAPIView(generics.CreateAPIView):
    """Client can book an appointment with a doctor"""
    serializer_class = serializers.BookingCreateDestroySerializer

    def perform_create(self, serializer):
        serializer.save(client=self.request.user.user_client)


class BookingListAPIView(generics.ListAPIView):
    """List of bookings for every doctor and every client"""
    queryset = Booking.objects.all()
    serializer_class = serializers.BookingListSerializer

    def get_queryset(self):
        if self.request.user.is_doctor:
            return Booking.objects.filter(visit__doctor=self.request.user.user_doctor).order_by('visit__date')
        else:
            return Booking.objects.filter(client=self.request.user.user_client).order_by('visit__date')


class BookingDestroyAPIView(generics.RetrieveDestroyAPIView):
    """Delete booking if hospital admin"""
    serializer_class = serializers.BookingCreateDestroySerializer
    queryset = Booking.objects.all()
    permission_classes = (IsBookingAdmin, )


class HospitalLikeCreateAPIView(generics.CreateAPIView):
    """Creating hospital likes"""
    serializer_class = serializers.HospitalLikesSerializer

    def check_like(self):
        user = self.request.user.user_client
        if HospitalLike.objects.filter(user=user, hospital=self.kwargs.get('pk')).exists():
            raise APIException('You already liked this hospital')

    def perform_create(self, serializer):
        self.check_like()
        serializer.save(user=self.request.user.user_client)
        liked_hospital = Hospital.objects.get(id=self.kwargs.get('pk'))
        liked_hospital.add_like()


class HospitalLikeDeleteAPIView(generics.DestroyAPIView):
    """Deleting hospital likes"""
    serializer_class = serializers.HospitalLikesSerializer

    def delete(self, request, *args, **kwargs):
        user = self.request.user.user_client
        try:
            like_obj = HospitalLike.objects.get(user=user, hospital=self.kwargs.get('pk'))
        except HospitalLike.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'Message': "Like doesn't exists"})
        liked_hospital = Hospital.objects.get(id=self.kwargs.get('pk'))

        like_obj.delete()
        liked_hospital.hospital_likes_amount -= 1
        liked_hospital.save()

        return Response(status=status.HTTP_200_OK)


class HospitalReviewCreateAPIView(generics.CreateAPIView):
    """Create a review for a hospital"""
    serializer_class = serializers.ReviewCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user.user_client
        hospital = get_object_or_404(Hospital, id=self.kwargs.get('pk'))
        if Review.objects.filter(hospital=hospital, author=user).exists():
            raise APIException('You have already commented this hospital.')
        average_ratings = Review.objects.filter(hospital=hospital).aggregate(Avg('rating__value'))

        if average_ratings['rating__value__avg'] is not None:
            hospital.rating = float(average_ratings['rating__value__avg'])
        else:
            hospital.rating = float(serializer.validated_data['rating'].value)
        hospital.reviews_amount += 1
        hospital.save()
        serializer.save(author=user)


class FeedbackCreateAPIView(generics.CreateAPIView):
    """Create a review after visiting doctor"""
    serializer_class = serializers.FeedbackCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user.user_client
        doctor = get_object_or_404(Doctor, id=self.kwargs.get('pk'))
        if Feedback.objects.filter(doctor=doctor, author=user).exists():
            raise APIException('You have already left a feedback.')
        average_ratings = Feedback.objects.filter(doctor=doctor).aggregate(Avg('rating__value'))

        if average_ratings['rating__value__avg'] is not None:
            doctor.rating = float(average_ratings['rating__value__avg'])
        else:
            doctor.rating = float(serializer.validated_data['rating'].value)
        doctor.feedbacks_amount += 1
        doctor.save()
        serializer.save(author=user)


class DoctorLikeCreateAPIView(generics.CreateAPIView):
    """Creating hospital likes"""
    serializer_class = serializers.DoctorLikesSerializer

    def check_like(self):
        user = self.request.user.user_client
        if DoctorLike.objects.filter(user=user, doctor=self.kwargs.get('pk')).exists():
            raise APIException('You already liked this doctor')

    def perform_create(self, serializer):
        self.check_like()
        serializer.save(user=self.request.user.user_client)
        liked_doctor = Doctor.objects.get(id=self.kwargs.get('pk'))
        liked_doctor.add_like()


class DoctorLikeDeleteAPIView(generics.DestroyAPIView):
    """Deleting hospital likes"""
    serializer_class = serializers.DoctorLikesSerializer

    def delete(self, request, *args, **kwargs):
        user = self.request.user.user_client
        try:
            like_obj = DoctorLike.objects.get(user=user, doctor=self.kwargs.get('pk'))
        except DoctorLike.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'Message': "Like doesn't exists"})
        liked_doctor = Doctor.objects.get(id=self.kwargs.get('pk'))
        like_obj.delete()
        liked_doctor.doctor_likes_amount -= 1
        liked_doctor.save()

        return Response(status=status.HTTP_200_OK)
