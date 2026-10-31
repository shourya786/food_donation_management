from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, FoodDonation

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ngo')  # Redirect to NGO page on successful login
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email.')
    return render(request, 'login.html')

def ngo_view(request):
    donations = FoodDonation.objects.all().order_by('-created_at')
    user_profiles = UserProfile.objects.select_related('user').all()
    return render(request, 'ngoo.html', {
        'donations': donations,
        'user_profiles': user_profiles,
    })

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'donor')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
        else:
            # Save standard Django User
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
            # Save user role in UserProfile table
            UserProfile.objects.create(user=user, role=role)
            
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
    return render(request, 'register.html')

@login_required
def dashboard_view(request):
    donations = FoodDonation.objects.filter(status='available').order_by('-created_at')
    user_profile = getattr(request.user, 'profile', None)
    return render(request, 'dashboard.html', {
        'donations': donations,
        'user_profile': user_profile
    })

@login_required
def create_donation_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        food_type = request.POST.get('food_type')
        pickup_address = request.POST.get('pickup_address')

        FoodDonation.objects.create(
            donor=request.user,
            title=title,
            description=description,
            quantity=quantity,
            food_type=food_type,
            pickup_address=pickup_address,
            status='available'
        )
        messages.success(request, 'Food donation posted successfully!')
        return redirect('dashboard')
    
    return render(request, 'create_donation.html')

@login_required
def claim_donation_view(request, donation_id):
    donation = get_object_or_404(FoodDonation, id=donation_id)
    if donation.status == 'available':
        donation.status = 'claimed'
        donation.claimed_by = request.user
        donation.save()
        messages.success(request, f'You have successfully claimed "{donation.title}".')
    else:
        messages.error(request, 'This donation is no longer available.')
    return redirect('dashboard')

def logout_view(request):
    logout(request)
    return redirect('login')

