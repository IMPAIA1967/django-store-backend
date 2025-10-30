from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.HomeView.as_view, name='home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view, name='product_detail'),
]