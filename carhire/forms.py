from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Location, VehicleType, Reservation

class SearchForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    vehicle_type = forms.ModelChoiceField(
        queryset=VehicleType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    pickup_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    dropoff_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['pickup_location', 'dropoff_location', 'pickup_date', 'dropoff_date']
        widgets = {
            'pickup_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'dropoff_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'pickup_location': forms.Select(attrs={'class': 'form-control'}),
            'dropoff_location': forms.Select(attrs={'class': 'form-control'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")