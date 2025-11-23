from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404
from .models import CustomUser, EmailVerificationToken
import secrets

from .forms import CustomUserCreationForm
from .models import CustomUser


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save(commit=False)  # Не сохраняем сразу
        user.is_active = False  # Пользователь не активен до подтверждения
        user.save()

        # Создаём токен
        token = secrets.token_hex(32)
        EmailVerificationToken.objects.create(user=user, token=token)


        # Отправляем письмо
        host = self.request.get_host()
        url = f'http://{host}{reverse("users:email_verification", kwargs={"token": token})}'

        send_mail(
            subject="Подтверждение почты",
            message=f"Привет! Перейди по ссылке для подтверждения почты:\n\n{url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(self.request, "Письмо с подтверждением отправлено на ваш email.")
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('catalog:home')


def email_verification(request, token):
    try:
        verification_token = get_object_or_404(EmailVerificationToken, token=token)
        user = verification_token.user
        user.is_active = True
        user.save()
        verification_token.delete()  # Удаляем токен после использования

        messages.success(request, "Email успешно подтверждён! Теперь вы можете войти.")
        return redirect('users:login')
    except Http404:
        messages.error(request, "Ссылка подтверждения недействительна или устарела.")
        return redirect('users:login')

