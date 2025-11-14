from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from . import views
from .views import email_verification

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("email-confirm/<str:token>", views.email_verification, name="email_verification"),
]