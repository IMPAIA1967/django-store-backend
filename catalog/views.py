from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm
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

    def get_queryset(self):
        return Product.objects.all()

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')


# def product_detail(request, pk):
#     """Отображает страницу одного товара по его ID (pk)."""
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'catalog/product_detail.html', {'product': product})



# def home(request):
#     """Главная страница — список всех товаров."""
#     products = Product.objects.select_related('category').all()
#     return render(request, 'catalog/home.html', {'products': products})