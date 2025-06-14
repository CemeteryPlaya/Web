from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from .models import TrackCode
from register.models import UserProfile

# Create your views here.
@login_required(login_url='login')
def profile(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = None

    # Последние 2 трек-кода пользователя
    last_two_codes = TrackCode.objects.filter(owner=user).order_by('-update_date')[:2]

    # Количество трек-кодов в статусе 'shipped_cn'
    user_added_count = TrackCode.objects.filter(owner=user, status='user_added').count()
    warehouse_cn_count = TrackCode.objects.filter(owner=user, status='warehouse_cn').count()
    shipped_cn_count = TrackCode.objects.filter(owner=user, status='shipped_cn').count()
    delivered_count = TrackCode.objects.filter(owner=user, status='delivered').count()

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'last_two_codes': last_two_codes,
        'user_added': user_added_count,
        'warehouse_cn': warehouse_cn_count,
        'shipped_cn_count': shipped_cn_count,
        'delivered': delivered_count,
    })

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required(login_url='login')
def track_codes_view(request):
    if request.method == 'POST':
        form = TrackCodeForm(request.POST)
        if form.is_valid():
            track_code = form.save(commit=False)
            track_code.owner = request.user
            track_code.status = 'user_added'
            track_code.save()
            messages.success(request, "Трек-код успешно добавлен.")
            return redirect('track_codes')
    else:
        form = TrackCodeForm()

    track_codes = TrackCode.objects.filter(owner=request.user).order_by('-update_date')
    return render(request, 'track_codes.html', {
        'track_codes': track_codes,
        'form': form
    })

@login_required
def add_track_code_view(request):
    if request.method == 'POST':
        form = TrackCodeForm(request.POST)
        if form.is_valid():
            track_code = form.save(commit=False)
            track_code.owner = request.user
            track_code.save()
            messages.success(request, "Трек-код успешно добавлен.")
            return redirect('track_codes')
    else:
        form = TrackCodeForm()
    return render(request, 'add_track_code.html', {'form': form})

def tracks(request):
    return render(request, "track_codes.html")

class TrackCodeForm(forms.ModelForm):
    class Meta:
        model = TrackCode
        fields = ['track_code', 'description']
        widgets = {
            'track_code': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2',
                'placeholder': 'Введите трек-код'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2',
                'placeholder': 'Описание посылки',
                'rows': 3
            }),
        }

@login_required
def settings(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = None

    return render(request, "settings.html", {
        'user': user,
        'profile': profile,
        'pickup': profile.pickup if profile else ''
    })

@login_required
@require_POST
def update_profile(request):
    user = request.user
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    pickup = request.POST.get('pickup')

    # Обновляем email пользователя
    if email:
        user.email = email
        user.save()

    # Обновляем или создаём профиль пользователя
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user)

    if phone:
        profile.phone = phone
    if pickup:
        profile.pickup = pickup
    profile.save()

    messages.success(request, "Профиль успешно обновлен.")
    return redirect('profile')