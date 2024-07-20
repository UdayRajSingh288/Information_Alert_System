from django.contrib import admin

from .models import User, Alert

admin.site.register(User)
admin.site.register(Alert)