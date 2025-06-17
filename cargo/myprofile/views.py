from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from collections import defaultdict
from .models import TrackCode, Receipt, ReceiptItem
from register.models import UserProfile
from decimal import Decimal

# Create your views here.
@login_required(login_url='login')
def profile(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = None

    last_two_codes = TrackCode.objects.filter(owner=user).order_by('-update_date')[:2]

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

    if email:
        user.email = email
        user.save()

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

@login_required
def delivered_trackcodes_by_date(request):
    delivered = TrackCode.objects.filter(owner=request.user, status='delivered')
    grouped = defaultdict(list)

    for track in delivered:
        price = (track.weight or Decimal("0")) * Decimal("1859")
        track.price = round(price, 2)
        grouped[track.update_date].append(track)

    result = {}
    for date, tracks in sorted(grouped.items(), reverse=True):
        total_weight = sum(t.weight or Decimal("0") for t in tracks)
        total_price = sum(t.price for t in tracks)
        result[date] = {
            'tracks': tracks,
            'total_weight': round(total_weight, 2),
            'total_price': round(total_price, 2)
        }

    # 👇 Автоматическое создание чека (один раз)
    if delivered.exists():
        from django.db.models import Q

        already_in_receipt = ReceiptItem.objects.filter(track_code__in=delivered).values_list('track_code_id', flat=True)
        new_tracks = delivered.exclude(id__in=already_in_receipt)

        if new_tracks.exists():
            total_weight = sum(t.weight or Decimal("0") for t in new_tracks)
            total_price = sum((t.weight or Decimal("0")) * Decimal("1859") for t in new_tracks)

            receipt = Receipt.objects.create(
                owner=request.user,
                total_weight=round(total_weight, 2),
                total_price=round(total_price, 2),
                is_paid=False
            )

            for track in new_tracks:
                ReceiptItem.objects.create(receipt=receipt, track_code=track)

    receipts = Receipt.objects.filter(owner=request.user).order_by('-created_at')

    return render(request, 'delivered_posts.html', {
        'grouped_trackcodes': result,
        'receipts': receipts
    })

@login_required
def generate_daily_receipt(request):
    delivered = TrackCode.objects.filter(owner=request.user, status='delivered')
    used_ids = ReceiptItem.objects.values_list('track_code_id', flat=True)
    unbilled = delivered.exclude(id__in=used_ids)

    if not unbilled.exists():
        messages.info(request, "Нет новых доставленных посылок для формирования чека.")
        return redirect('delivered_posts')

    total_weight = sum(track.weight or Decimal("0") for track in unbilled)
    total_price = total_weight * Decimal("1859")

    receipt = Receipt.objects.create(
        owner=request.user,
        total_weight=round(total_weight, 2),
        total_price=round(total_price, 2)
    )

    for track in unbilled:
        ReceiptItem.objects.create(receipt=receipt, track_code=track)

    messages.success(request, f"Создан чек #{receipt.id} на сумму {receipt.total_price} тг.")
    return redirect('receipt_list')

@login_required
def receipt_list(request):
    receipts = Receipt.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'receipts.html', {'receipts': receipts})