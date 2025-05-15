from django.contrib import admin
from .models import Registration

# Register your models here.
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('login', 'phone', 'pickup', 'created_at')
    search_fields = ('login', 'phone', 'pickup')
    list_filter = ('pickup', 'created_at')