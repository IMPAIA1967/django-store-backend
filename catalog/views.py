from django.shortcuts import render, get_object_or_404
from .models import Product


def product_detail(request, pk):
    """Отображает страницу одного товара по его ID (pk)."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def home(request):
    """Главная страница — список всех товаров."""
    products = Product.objects.select_related('category').all()
    return render(request, 'catalog/home.html', {'products': products})