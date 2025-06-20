from django.contrib import admin
from .models import TrackCode, Receipt, ReceiptItem

# Register your models here.
@admin.register(TrackCode)
class TrackCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'track_code', 'owner', 'update_date', 'status', 'description', 'weight')
    search_fields = ('id', 'track_code', 'owner')
    list_filter = ('status', 'update_date')

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'created_at', 'is_paid', 'total_weight', 'total_price')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('owner__username',)

@admin.register(ReceiptItem)
class ReceiptItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'receipt', 'track_code')