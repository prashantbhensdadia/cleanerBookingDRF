from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(City)
admin.site.register(Cleaner)
admin.site.register(Appointment)
