from django.contrib import admin

from .models import Hackathon, Submission, HackathonRegistration

# Register your models here.

admin.site.register(Hackathon)
admin.site.register(Submission)
admin.site.register(HackathonRegistration)
