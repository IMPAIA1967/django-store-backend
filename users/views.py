from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

from .forms import CustomUserCreationForm

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # автоматический вход после регистрации

        # Отправка приветственного письма
        send_mail(
            subject='Добро пожаловать!',
            message='Спасибо за регистрацию на нашем сайте!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('catalog:home')


