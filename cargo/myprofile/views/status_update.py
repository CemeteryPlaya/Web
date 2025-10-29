from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from myprofile.models import TrackCode, Notification
from register.models import UserProfile
from decimal import Decimal
from datetime import datetime

# Create your views here.
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
            track = None
            try:
                track = TrackCode.objects.get(track_code=code)
                old_status = track.status

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

                if old_status != status:
                    Notification.objects.create(
                        user=track.owner,
                        message=f"📦 Ваш трек-код {track.track_code} обновлен: {track.get_status_display()}"
                    )

            except TrackCode.DoesNotExist:
                if status == 'delivered':
                    try:
                        user = User.objects.get(username=usernames[i])
                        UserProfile.objects.get(user=user)
                        track = TrackCode.objects.create(
                            track_code=code,
                            status=status,
                            update_date=update_date,
                            owner=user,
                            weight=Decimal(weights[i])
                        )
                        created += 1

                        Notification.objects.create(
                            user=user,
                            message=f"📦 Добавлен новый трек-код {track.track_code}: {track.get_status_display()}"
                        )

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