from django.contrib import admin
from .models import Location, VehicleType, Vehicle, Reservation

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'address']
    search_fields = ['name', 'city']

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'year', 'vehicle_type', 'location', 'daily_rate', 'is_available']
    list_filter = ['vehicle_type', 'location', 'is_available', 'condition']
    search_fields = ['make', 'model']
    list_editable = ['is_available', 'daily_rate']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['confirmation_number', 'user', 'vehicle', 'pickup_date', 'dropoff_date', 'status', 'total_amount']
    list_filter = ['status', 'pickup_date', 'created_at']
    search_fields = ['confirmation_number', 'user__username', 'vehicle__make', 'vehicle__model']
    readonly_fields = ['confirmation_number', 'created_at']