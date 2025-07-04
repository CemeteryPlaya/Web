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
from django.contrib import admin
from django.urls import path, include, re_path
from mainview import views as mainview_views

urlpatterns = [
    re_path(r"^mainview/", include('mainview.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    re_path(r"^register/", include('register.urls')),
    re_path(r"^profile/", include('myprofile.urls')),
    # Admin URL
    path('admin/', admin.site.urls),
    # Main application URLs
    path('', mainview_views.index, name='home'),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)