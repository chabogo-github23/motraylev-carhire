from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Vehicle, Location, VehicleType, Reservation
from .forms import SearchForm, ReservationForm, CustomUserCreationForm

def home(request):
    """Landing page with search form"""
    form = SearchForm()
    return render(request, 'carhire/home.html', {'form': form})

def search_vehicles(request):
    """Search for available vehicles"""
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            vehicle_type = form.cleaned_data['vehicle_type']
            pickup_date = form.cleaned_data['pickup_date']
            dropoff_date = form.cleaned_data['dropoff_date']
            
            # Calculate total days
            total_days = (dropoff_date - pickup_date).days
            if total_days <= 0:
                messages.error(request, "Dropoff date must be after pickup date")
                return render(request, 'carhire/home.html', {'form': form})
            
            # Find available vehicles
            vehicles = Vehicle.objects.filter(
                location=location,
                vehicle_type=vehicle_type,
                is_available=True
            )
            
            # Check for conflicting reservations
            available_vehicles = []
            for vehicle in vehicles:
                conflicting_reservations = Reservation.objects.filter(
                    vehicle=vehicle,
                    status__in=['pending', 'confirmed'],
                    pickup_date__lt=dropoff_date,
                    dropoff_date__gt=pickup_date
                )
                if not conflicting_reservations.exists():
                    available_vehicles.append(vehicle)
            
            if not available_vehicles:
                messages.warning(request, "No vehicles available for the selected criteria. Please try different dates or location.")
                return render(request, 'carhire/home.html', {'form': form})
            
            # Store search criteria in session
            request.session['search_data'] = {
                'location_id': location.id,
                'vehicle_type_id': vehicle_type.id,
                'pickup_date': pickup_date.isoformat(),
                'dropoff_date': dropoff_date.isoformat(),
                'total_days': total_days
            }
            
            return render(request, 'carhire/vehicle_list.html', {
                'vehicles': available_vehicles,
                'search_data': request.session['search_data'],
                'total_days': total_days
            })
    
    form = SearchForm()
    return render(request, 'carhire/home.html', {'form': form})

def vehicle_detail(request, vehicle_id):
    """Show vehicle details"""
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    search_data = request.session.get('search_data')
    
    if not search_data:
        messages.error(request, "Please search for vehicles first")
        return redirect('home')
    
    total_amount = vehicle.daily_rate * search_data['total_days'] + 1000  # Including reservation fee
    
    return render(request, 'carhire/vehicle_detail.html', {
        'vehicle': vehicle,
        'search_data': search_data,
        'total_amount': total_amount
    })

@login_required
def make_reservation(request, vehicle_id):
    """Make a reservation for a vehicle"""
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    search_data = request.session.get('search_data')
    
    if not search_data:
        messages.error(request, "Please search for vehicles first")
        return redirect('home')
    
    if request.method == 'POST':
        # Create reservation
        pickup_date = datetime.fromisoformat(search_data['pickup_date'])
        dropoff_date = datetime.fromisoformat(search_data['dropoff_date'])
        total_days = search_data['total_days']
        total_amount = vehicle.daily_rate * total_days + 1000
        
        reservation = Reservation.objects.create(
            user=request.user,
            vehicle=vehicle,
            pickup_location_id=search_data['location_id'],
            dropoff_location_id=search_data['location_id'],  # Same location for simplicity
            pickup_date=pickup_date,
            dropoff_date=dropoff_date,
            total_days=total_days,
            total_amount=total_amount,
            status='pending'
        )
        
        # Clear search data from session
        if 'search_data' in request.session:
            del request.session['search_data']
        
        messages.success(request, f"Reservation created successfully! Confirmation number: {reservation.confirmation_number}")
        return redirect('reservation_confirmation', reservation_id=reservation.id)
    
    total_amount = vehicle.daily_rate * search_data['total_days'] + 1000
    
    return render(request, 'carhire/make_reservation.html', {
        'vehicle': vehicle,
        'search_data': search_data,
        'total_amount': total_amount
    })

@login_required
def reservation_confirmation(request, reservation_id):
    """Show reservation confirmation"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    return render(request, 'carhire/reservation_confirmation.html', {'reservation': reservation})

@login_required
def my_reservations(request):
    """Show user's reservations"""
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'carhire/my_reservations.html', {'reservations': reservations})

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def about(request):
    """About page with company information"""
    return render(request, 'carhire/about.html')