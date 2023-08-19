from django.contrib import admin
from .models import User

class RefAdmin(admin.ModelAdmin):
    readonly_fields =("phone_number",)

admin.site.register(User, RefAdmin)
