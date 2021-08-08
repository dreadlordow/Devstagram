from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include('devstagram.registration.urls')),
    path('', include('devstagram.mainsite.urls')),
    path('', include('devstagram.async_chat.urls')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

