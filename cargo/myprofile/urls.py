"""
URL configuration for cargo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('track-codes/', views.track_codes_view, name='track_codes'),
    path('settings/', views.settings, name='settings'),
    path('update/', views.update_profile, name='update_profile'),
    path('', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('delivered-posts/', views.delivered_trackcodes_by_date, name='delivered_posts'),
    path('receipts/', views.receipt_list, name='receipt_list'),
    path('generate-receipt/', views.generate_daily_receipt, name='generate_receipt'),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)