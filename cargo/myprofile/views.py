from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django import forms
from collections import defaultdict
from .models import TrackCode, Receipt, ReceiptItem, Notification
from register.models import UserProfile
from decimal import Decimal
from datetime import datetime

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

@require_POST
@login_required
def pay_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id, user=request.user)
    if not receipt.is_paid:
        receipt.is_paid = True  # временно, потом можно подключить оплату
        receipt.save()
    return redirect('delivered_posts')

@login_required
def update_tracks(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        update_date_str = request.POST.get('update_date')
        track_codes_raw = request.POST.get('track_codes', '').strip()
        usernames_raw = request.POST.get('owner_usernames', '').strip()
        weights_raw = request.POST.get('weights', '').strip()

        if not status or not update_date_str or not track_codes_raw:
            messages.error(request, "Заполните все обязательные поля.")
            return redirect('update_tracks')

        try:
            update_date = datetime.strptime(update_date_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Неверный формат даты.")
            return redirect('update_tracks')

        track_codes = [line.strip() for line in track_codes_raw.splitlines() if line.strip()]

        if status == 'delivered':
            usernames = [line.strip() for line in usernames_raw.splitlines() if line.strip()]
            weights = [line.strip() for line in weights_raw.splitlines() if line.strip()]

            if len(track_codes) != len(usernames) or len(track_codes) != len(weights):
                messages.error(request, "Количество трек-кодов, пользователей и весов должно совпадать.")
                return redirect('update_tracks')

        updated = 0
        created = 0

        for i, code in enumerate(track_codes):
            try:
                track = TrackCode.objects.get(track_code=code)
                track.status = status
                track.update_date = update_date
                if status == 'delivered':
                    try:
                        user = User.objects.get(username=usernames[i])
                        UserProfile.objects.get(user=user)  # проверка существования
                        track.owner = user
                        track.weight = Decimal(weights[i])
                    except (User.DoesNotExist, UserProfile.DoesNotExist):
                        messages.error(request, f"Пользователь '{usernames[i]}' не найден.")
                        return redirect('update_tracks')
                track.save()
                updated += 1
            except TrackCode.DoesNotExist:
                if status == 'delivered':
                    try:
                        user = User.objects.get(username=usernames[i])
                        UserProfile.objects.get(user=user)
                        TrackCode.objects.create(
                            track_code=code,
                            status=status,
                            update_date=update_date,
                            owner=user,
                            weight=Decimal(weights[i])
                        )
                        created += 1
                    except (User.DoesNotExist, UserProfile.DoesNotExist):
                        messages.error(request, f"Пользователь '{usernames[i]}' не найден.")
                        return redirect('update_tracks')
                else:
                    messages.warning(request, f"Трек-код '{code}' не найден и не создан.")
        
        if updated:
            messages.success(request, f"Обновлено: {updated}")
        if created:
            messages.success(request, f"Создано новых: {created}")

        return redirect('update_tracks')

    return render(request, "update_tracks.html", {
        'status_choices': TrackCode.STATUS_CHOICES
    })

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'myprofile/notifications.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, owner=request.user)
    notif.status = "Просмотрено"
    notif.save()
    return redirect('notifications')

def notifications_context(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications_count': unread_count}
    return {}

@login_required
def mark_notifications_as_read(request):
    if request.method == "POST":
        Notification.objects.filter(owner=request.user, is_read=False).update(is_read=True)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)