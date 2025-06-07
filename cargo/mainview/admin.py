from django.contrib import admin
from .models import Registration, TrackCode

# Register your models here.
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('login', 'phone', 'pickup', 'created_at')
    search_fields = ('login', 'phone', 'pickup')
    list_filter = ('pickup', 'created_at')

@admin.register(TrackCode)
class TrackCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'track_code', 'owner', 'update_date', 'status', 'description', 'weight')
    search_fields = ('id', 'track_code', 'owner')
    list_filter = ('status', 'update_date')