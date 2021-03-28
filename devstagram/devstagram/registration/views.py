from functools import cache
from random import randint

from django.contrib.auth import views as auth_views, authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.decorators.http import require_POST

from devstagram.mainsite.models import TwoFactorAuthMsg
from devstagram.registration.forms import RegisterForm


class RegisterView(views.CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return reverse_lazy('profile', kwargs={'slug': username})


class SignInView(auth_views.LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = User.objects.get(username=username)
        if user.userauth.two_factor_auth:
            hash_url, code = self.create_hash_url_and_code(username)
            self.send_email_with_code(user, code)
            context = {
                'hash_url': hash_url,
                'user': user,
                'password': password,
            }
            return render(self.request, 'registration/twofactor.html', context)

        return super().form_valid(form)

    @staticmethod
    def create_hash_url_and_code(username):
        hash_url = f'{username}' + str(hash(str(randint(1, 999))))
        code = ''

        # Generate random code
        for _ in range(6):
            code += str(randint(1, 9))
        tfa = TwoFactorAuthMsg(hash_url=hash_url, two_factor_code=int(code))
        tfa.save()
        return hash_url, code

    @staticmethod
    def send_email_with_code(user, code):
        send_mail(
            'Devstagram authentication code',
            f'Your authentication code is {code}',
            'georgipavlov910@gmail.com',
            [f'{user.email}', ],
            fail_silently=False
        )

@require_POST
def two_factor(request, slug):
    code = int(request.POST['2fa'])
    username = request.POST['username']
    user = User.objects.get(username=username)
    password = request.POST['password']
    tfa = TwoFactorAuthMsg.objects.filter(hash_url=slug).last()
    received_code = tfa.two_factor_code
    if code == received_code:
        tfa.delete()
        login(request, user)
        return redirect('index')
    tfa.delete()
    return redirect('signin')


class SignOutView(auth_views.LogoutView):
    redirect_field_name = reverse_lazy('landing page')