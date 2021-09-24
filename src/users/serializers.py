from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .models import Doctor, Client, MyUser, HospitalAdmin
from hospital.models import Feedback


class UserSerializer(serializers.ModelSerializer):
    """Serializer for custom user"""
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'token']


class ClientRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for client's registration"""
    user = UserSerializer()

    class Meta:
        model = Client
        fields = [
            'user', 'first_name', 'last_name',
            'phone_number', 'gender', 'age'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = MyUser.objects.create_user(**user_data, is_doctor=False, is_hospital_admin=False)
        client = Client.objects.create_client(user=user, **validated_data)
        return client


class DoctorRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for doctor's registration"""
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = ['user', 'first_name', 'last_name']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = MyUser.objects.create_user(**user_data, is_doctor=True, is_hospital_admin=False)
        doctor = Doctor.objects.create_doctor(user=user, **validated_data)
        return doctor


class HospitalAdminRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for hospital admin registration"""
    user = UserSerializer()

    class Meta:
        model = HospitalAdmin
        fields = ['user', 'hospital', 'first_name', 'last_name']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = MyUser.objects.create_user(**user_data, is_doctor=False, is_hospital_admin=True)
        hospital_admin = HospitalAdmin.objects.create_hospital_admin(user=user, **validated_data)
        return hospital_admin


class FeedbackListSerializer(serializers.ModelSerializer):
    """Serializer for listing feedbacks"""

    created_at = serializers.DateTimeField(format='%c')

    class Meta:
        model = Feedback
        fields = ['author', 'text', 'created_at']


class DoctorProfileSerializer(serializers.ModelSerializer):
    """Serializer for doctor's profile"""
    feedbacks = FeedbackListSerializer(many=True)

    class Meta:
        model = Doctor
        exclude = ['doctor_likes_amount', 'user']


class ClientProfileSerializer(serializers.ModelSerializer):
    """Serializer for client profile"""

    class Meta:
        model = Client
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)
    date = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('email', None).lower()
        password = data.get('password', None)

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                raise serializers.ValidationError('This user has been deactivated.')

            if MyUser.objects.filter(email=username).exists():
                user_object = MyUser.objects.get(email=username)
            else:
                raise serializers.ValidationError(
                    'User with given email and password does not exists'
                )

            return {
                'email': user_object.email,
                'token': user_object.token,
            }
