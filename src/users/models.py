import datetime
import time

import jwt
from django.conf import settings

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):

    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_user(self, email, is_hospital_admin, is_doctor, password=None):
        """Create and return a `User` with an email, username and password."""
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email), is_doctor=is_doctor, is_hospital_admin=is_hospital_admin)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, False, False, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class ClientManager(BaseUserManager):

    def create_client(self, user, first_name, last_name, phone_number, gender, age):
        client = Client(
            user=user, first_name=first_name, phone_number=phone_number,
            last_name=last_name, gender=gender, age=age
        )
        client.save()
        return client


class DoctorManager(BaseUserManager):

    def create_doctor(self, user, first_name, last_name):
        doctor = Doctor(user=user, first_name=first_name, last_name=last_name)
        doctor.save()
        return doctor


class HospitalAdminManager(BaseUserManager):

    def create_hospital_admin(self, user, hospital, first_name, last_name):
        hospital_admin = HospitalAdmin(user=user, hospital=hospital, first_name=first_name, last_name=last_name)
        hospital_admin.save()
        return hospital_admin


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_doctor = models.BooleanField(default=False)
    is_hospital_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.datetime.now() + datetime.timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': str(time.mktime(dt.timetuple()))[:-2]
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class Client(models.Model):
    """Client's profile"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_client', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(default=18)

    objects = ClientManager()

    def __str__(self):
        return f'{self.first_name}'

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True


class Doctor(models.Model):
    """Doctor's profile"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_doctor', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255, null=True, blank=True)
    proficiency = models.CharField(max_length=255, null=True, blank=True)
    experience = models.PositiveIntegerField(default=1)
    photo = models.ImageField(upload_to='doctors/')
    biography = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hospital = models.ForeignKey('hospital.Hospital', related_name='doctors',
                                 on_delete=models.CASCADE, null=True, blank=True
                                 )
    address = models.CharField(max_length=255, null=True, blank=True)
    specialization = models.ManyToManyField('hospital.Specialization', blank=True)
    education = models.TextField(null=True, blank=True)
    courses = models.TextField(null=True, blank=True)
    procedures = models.TextField(null=True, blank=True)
    doctor_likes_amount = models.PositiveIntegerField(default=0)
    visit_duration = models.PositiveIntegerField(null=True, blank=True)
    rating = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    feedbacks_amount = models.PositiveIntegerField(default=0)

    objects = DoctorManager()

    def __str__(self):
        return f'Doctor: {self.first_name} {self.last_name}'

    def add_like(self):
        self.doctor_likes_amount += 1
        self.save()

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True


class HospitalAdmin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='user_hospital_admin',
        on_delete=models.CASCADE
    )
    hospital = models.ForeignKey(
        'hospital.Hospital', related_name='hospital_admin',
        on_delete=models.CASCADE, blank=True, null=True
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    objects = HospitalAdminManager()

    def __str__(self):
        return f'Admin: {self.first_name} {self.last_name}'

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True
