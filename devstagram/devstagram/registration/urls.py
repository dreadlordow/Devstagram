from django.urls import path

from devstagram.registration.views import RegisterView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
]

from .receivers import *