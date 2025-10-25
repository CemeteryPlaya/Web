from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from collections import defaultdict
from myprofile.models import TrackCode, Receipt, ReceiptItem
from decimal import Decimal

# Create your views here.
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