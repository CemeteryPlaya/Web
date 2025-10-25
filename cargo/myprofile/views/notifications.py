from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from myprofile.models import Notification

# Create your views here.
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