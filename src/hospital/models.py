from django.db import models
from django.core.validators import RegexValidator

from users.models import Doctor, Client


SCHEDULE_CHOICES = (
    ('Every day', 'Every day'),
    ('Every week', 'Every week'),
    ('Except weekend', 'Except weekend'),
    ('Once', 'Once')
)


class Hospital(models.Model):
    """Hospital objects"""

    title = models.CharField(max_length=255, unique=True)
    short_title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    logo = models.ImageField(null=True, upload_to='hospitals/')
    description = models.TextField()
    opening_time = models.TimeField(auto_now=False, auto_now_add=False)
    closing_time = models.TimeField(auto_now=False, auto_now_add=False)
    address = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    services = models.ManyToManyField('Service')
    reviews_amount = models.PositiveIntegerField(default=0)
    hospital_likes_amount = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(default=0, max_digits=3, decimal_places=2)

    def __str__(self):
        return self.short_title

    def add_like(self):
        self.hospital_likes_amount += 1
        self.save()


class Service(models.Model):
    """Services provided by each hospital"""

    title = models.CharField(max_length=255)
    url = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class RatingStar(models.Model):
    """"Available amounts of stars for one comment"""
    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.value}'


class Review(models.Model):
    """Client can leave a review after visiting the hospital"""

    author = models.ForeignKey(Client, on_delete=models.CASCADE)
    rating = models.ForeignKey(RatingStar, related_name='hospital_review', on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class HospitalLike(models.Model):
    """Likes for hospitals"""

    user = models.ForeignKey(Client, related_name='hospital_likes', on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, related_name='likes', on_delete=models.CASCADE)


class Specialization(models.Model):
    """Doctor services specialization"""

    title = models.CharField(max_length=255)
    url = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    """Client can leave a feedback after visiting a doctor"""

    author = models.ForeignKey(Client, on_delete=models.CASCADE)
    rating = models.ForeignKey(RatingStar, related_name='client_feedback', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey(Doctor, related_name='feedbacks', on_delete=models.CASCADE)


class DoctorLike(models.Model):
    """Likes for doctors"""

    user = models.ForeignKey(Client, related_name='doctor_likes', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='likes', on_delete=models.CASCADE)


class Schedule(models.Model):
    """Doctor's Schedule"""
    doctor = models.ForeignKey(Doctor, related_name='schedule', on_delete=models.CASCADE)
    time_from = models.TimeField(auto_now=False, auto_now_add=False)
    time_to = models.TimeField(auto_now=False, auto_now_add=False)
    date = models.DateField()
    periodicity = models.CharField(max_length=255, choices=SCHEDULE_CHOICES, null=True, blank=True)

    class Meta:
        unique_together = ['doctor', 'date']


class Visit(models.Model):
    """Visits for each doctor which clients can book"""
    doctor = models.ForeignKey(Doctor, related_name='visits', on_delete=models.CASCADE)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    date = models.DateField()

    class Meta:
        unique_together = ['doctor', 'time', 'date']

    def __str__(self):
        return f'{self.id}. Doctor: {self.doctor.first_name}, Date: {self.date}, Time: {self.time}'


class Booking(models.Model):
    """Model for booking a visit to doctor"""
    visit = models.OneToOneField(Visit, related_name='booking_visit', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name='clients', on_delete=models.CASCADE)
    service = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.client} : {self.visit}'
