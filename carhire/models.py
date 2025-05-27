from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50, default='Nairobi')  # Add default here
    address = models.TextField()
    
    def __str__(self):
        return f"{self.name}, {self.city}"

class VehicleType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Vehicle(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    mileage = models.IntegerField()
    condition = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair')
    ])
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pickup_reservations')
    dropoff_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='dropoff_reservations')
    pickup_date = models.DateTimeField()
    dropoff_date = models.DateTimeField()
    total_days = models.IntegerField()
    reservation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    confirmation_number = models.CharField(max_length=20, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.confirmation_number:
            self.confirmation_number = f"CAR{self.id or ''}{timezone.now().strftime('%Y%m%d%H%M')}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Reservation {self.confirmation_number} - {self.vehicle}"