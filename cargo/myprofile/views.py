from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import TrackCode
from register.models import UserProfile

# Create your views here.
@login_required(login_url='login')
def profile(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = None  # можно создать при необходимости
    return render(request, 'profile.html', {'user': user, 'profile': profile})

@login_required
def profile_view(request):
    return render(request, 'profile.html')

def track_codes_view(request):
    track_codes = TrackCode.objects.filter(owner=request.user).order_by('-update_date')
    return render(request, 'track_codes.html', {'track_codes': track_codes})

def tracks(request):
    return render(request, "track_codes.html")

