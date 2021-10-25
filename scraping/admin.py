from django.contrib import admin

from .models import Review, Platform


# Register your models here.
admin.site.register(Review)
admin.site.register(Platform)