from django.urls import path

from devstagram.registration.views import RegisterView, SignInView, two_factor

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('2fa/<str:slug>', two_factor, name='2fa'),
]

from .receivers import *