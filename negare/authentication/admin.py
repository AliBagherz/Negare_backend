from django.contrib import admin

# Register your models here.
from authentication.models import AppUser

admin.site.register(AppUser)
