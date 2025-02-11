"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from .views import send_push_notification, send_perticular_user


from .error_handler import custom_404
handler404 = custom_404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restorent.urls')),
    path('api/', include('restorent.api_urls')),
    path("send-notification/", send_push_notification, name="send_notification"),
    path("send-user/<int:pk>", send_perticular_user, name="send_perticular_user"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)