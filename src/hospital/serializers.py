from rest_framework import serializers

from rest_framework.reverse import reverse
from users.models import Doctor

from .models import Hospital, Review, Specialization, Service, Schedule, Visit, Booking, HospitalLike, Feedback, \
    DoctorLike


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating reviews"""

    class Meta:
        model = Review
        fields = ['author', 'rating', 'hospital', 'text']


class ReviewListSerializer(serializers.ModelSerializer):
    """Serializer for reviews"""

    created_at = serializers.DateTimeField(format='%c')

    class Meta:
        model = Review
        fields = ['author', 'text', 'created_at']


class FeedbackCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating feedback for every doctor"""

    class Meta:
        model = Feedback
        fields = ['author', 'rating', 'doctor', 'text']


class DoctorListSerializer(serializers.ModelSerializer):
    """Serializer for doctors"""

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name']


class HospitalListSerializer(serializers.ModelSerializer):
    """Serializer for hospitals"""
    opening_time = serializers.TimeField(format='%I:%M %p', input_formats='%I:%M %p')
    closing_time = serializers.TimeField(format='%I:%M %p', input_formats='%I:%M %p')

    class Meta:
        model = Hospital
        fields = ['title', 'type', 'logo', 'description', 'opening_time', 'closing_time', 'address',
                  'phone_number', 'hospital_likes_amount', 'reviews_amount']


class HospitalDetailSerializer(serializers.ModelSerializer):
    """Serializer for hospital details"""

    opening_time = serializers.TimeField(format='%I:%M %p', input_formats='%I:%M %p')
    closing_time = serializers.TimeField(format='%I:%M %p', input_formats='%I:%M %p')
    reviews = ReviewListSerializer(many=True)
    doctors = DoctorListSerializer(many=True, read_only=True)
    services = serializers.SlugRelatedField(slug_field='title', many=True, read_only=True)

    class Meta:
        model = Hospital
        fields = '__all__'


class SpecializationListSerializer(serializers.ModelSerializer):
    """"Serializer for list of doctor's Specializations"""
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('specializations', kwargs={"url": obj}))

    class Meta:
        model = Specialization
        fields = '__all__'


class ServiceListSerializer(serializers.ModelSerializer):
    """"Serializer for list of hospital's Services"""
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('hospital-services', kwargs={"url": obj}))

    class Meta:
        model = Service
        fields = ['title', 'url']


class ScheduleSerializer(serializers.ModelSerializer):
    """Serializer for doctor's schedule"""
    date = serializers.DateField(format='%d/%m/%y %H:%M:%S')
    doctor = DoctorListSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'


class VisitSerializer(serializers.ModelSerializer):
    """Serializer for visits(timespaces when client can visit a doctor)"""
    date = serializers.TimeField(format='%A')
    time = serializers.TimeField(format='%H:%M')
    doctor = serializers.SlugRelatedField(slug_field='last_name', read_only=True)

    class Meta:
        model = Visit
        fields = ['id', 'date', 'time', 'doctor']


class BookingCreateDestroySerializer(serializers.ModelSerializer):
    """Serializer for creating or deleting bookings"""

    class Meta:
        model = Booking
        fields = ['visit', 'service']


class BookingListSerializer(serializers.ModelSerializer):
    """Serializer for listing bookings"""
    client = serializers.SlugRelatedField(slug_field='first_name', read_only=True)

    visit = serializers.SerializerMethodField()

    def get_visit(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('visit-detail', kwargs={"pk": obj.visit.id}))

    class Meta:
        model = Booking
        fields = ['visit', 'client', 'service']


class DoctorLikesSerializer(serializers.ModelSerializer):
    """"Serializer for hospital likes"""

    class Meta:
        model = DoctorLike
        fields = ['doctor']


class HospitalLikesSerializer(serializers.ModelSerializer):
    """"Serializer for hospital likes"""

    class Meta:
        model = HospitalLike
        fields = ['hospital']
