from django.contrib import admin
from .models import TrackCode

# Register your models here.
@admin.register(TrackCode)
class TrackCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'track_code', 'owner', 'update_date', 'status', 'description', 'weight')
    search_fields = ('id', 'track_code', 'owner')
    list_filter = ('status', 'update_date')