from django.urls import path
from . import views
from .models import Car, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import CarForm , OrderForm
from django.utils.dateparse import parse_date
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
def home_view(request):
 return render(request, 'carss/home.html')
    
# Create your views here.
def browse_cars(request):
    cars = Car.objects.all()
    return render(request, 'carss/browse_cars.html', {'cars': cars})
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("Login view accessed")
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('browse_cars')  # Redirect to a page after login
        else:
            print("Invalid credentials")
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect back to login page on failure

    return render(request, 'carss/login.html')  # Render the login page

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')  # matches name="password"
        password2 = request.POST.get('password_confirmation')  # matches name="password_confirmation"

        if not username or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('browse_cars')  # or any other page after registration

    return render(request, 'carss/signup.html')
             
             
        
        
          
@login_required
def profile_view(request):
    return render(request, 'carss/profile.html')
            
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to login after logout

def group_required(SELLERS):
    def in_group(user):
        return user.is_authenticated and user.groups.filter(name=SELLERS).exists()
    return user_passes_test(in_group)

@login_required
def list_car_view(request):
    if not request.user.groups.filter(name='SELLERS').exists():
        return HttpResponseForbidden("You do not have permission to access this page.If you want to become a seller, please contact the admin with your credentials at niktsanth@gmail.com thank you.")
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('browse_cars')
    else:
        form = CarForm()
    return render(request, 'carss/listur.html', {'form': form})

@login_required
def place_order(request, car_id=None):
    car = get_object_or_404(Car, id=car_id)
    now = datetime.now()

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        if start_date_str and start_date_str < now.strftime('%Y-%m-%d'):
            messages.error(request, "Start date cannot be in the past.")
            return redirect('browse_cars')

        if not start_date_str or not end_date_str:
            messages.error(request, "Please provide both start and end dates.")
            return redirect('browse_cars')

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date:
            messages.error(request, "Invalid date format.")
            return redirect('browse_cars')

        if end_date < start_date:
            messages.error(request, "End date cannot be before start date.")
            return redirect('browse_cars')

        order = Order(
            user=request.user,
            car=car,
            start_date=start_date,
            end_date=end_date
        )
        order.save()  # This should save the order in DB

        return render(request, 'carss/order_success.html', {'order': order})

    return redirect('browse_cars')

