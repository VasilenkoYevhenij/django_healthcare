from django.contrib import admin
from . import models


@admin.register(models.Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'time', 'date')
    list_display_links = ('doctor', )
    list_filter = ('date',)
    search_fields = ('doctor__first_name',)


admin.site.register(models.Service)
admin.site.register(models.Specialization)
admin.site.register(models.Hospital)
admin.site.register(models.Review)
admin.site.register(models.Feedback)
admin.site.register(models.Booking)
admin.site.register(models.DoctorLike)
admin.site.register(models.HospitalLike)
admin.site.register(models.Schedule)
admin.site.register(models.RatingStar)
