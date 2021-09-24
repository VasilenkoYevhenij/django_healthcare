from django.db.models import Avg
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Visit, Schedule, Review, Feedback


@receiver(post_delete, sender=Schedule)
def delete_visits(sender, instance, **kwargs):
    if sender == Schedule:
        Visit.objects.filter(doctor=instance.doctor, date=instance.date).delete()


@receiver(post_delete, sender=Review)
def decrement_reviews_amount(sender, instance, **kwargs):
    if sender == Review:
        hospital = instance.hospital
        average_ratings = Review.objects.filter(hospital=hospital).aggregate(Avg('rating__value'))
        hospital.reviews_amount -= 1
        if average_ratings['rating__value__avg'] is not None:
            hospital.rating = float(average_ratings['rating__value__avg'])
        else:
            hospital.rating = 0
        hospital.save()


@receiver(post_delete, sender=Feedback)
def decrement_reviews_amount(sender, instance, **kwargs):
    if sender == Feedback:
        doctor = instance.doctor
        average_ratings = Feedback.objects.filter(doctor=doctor).aggregate(Avg('rating__value'))
        doctor.feedbacks_amount -= 1
        if average_ratings['rating__value__avg'] is not None:
            doctor.rating = float(average_ratings['rating__value__avg'])
        else:
            doctor.rating = 0
        doctor.save()
