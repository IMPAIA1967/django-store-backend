from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Product


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'catalog/product_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj


class HomeView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'catalog/home.html'






# def product_detail(request, pk):
#     """Отображает страницу одного товара по его ID (pk)."""
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'catalog/product_detail.html', {'product': product})



# def home(request):
#     """Главная страница — список всех товаров."""
#     products = Product.objects.select_related('category').all()
#     return render(request, 'catalog/home.html', {'products': products})