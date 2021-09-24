from django.contrib import admin

from .models import Client, Doctor, HospitalAdmin, MyUser


admin.site.register(Client)
admin.site.register(Doctor)
admin.site.register(HospitalAdmin)
admin.site.register(MyUser)
