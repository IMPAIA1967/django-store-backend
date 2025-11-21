from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ProductForm
from .models import Product, Category
from .services import get_published_products, get_products_by_category, invalidate_published_products_cache, invalidate_category_cache,



class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'catalog/product_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Проверяем, является ли пользователь владельцем или модератором
        is_owner = self.request.user == product.owner
        is_moderator = (
                self.request.user.is_authenticated and
                self.request.user.groups.filter(name='Модератор продуктов').exists()
        )

        context['can_edit_or_delete'] = is_owner or is_moderator
        context['can_unpublish'] = self.request.user.has_perm('catalog.can_unpublish_product')

        return context

class HomeView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'catalog/home.html'

    def get_queryset(self):
        # Используем кешированную функцию из services.py
        return get_published_products()

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        # Сбрасываем кеш списка опубликованных продуктов
        invalidate_published_products_cache()
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_queryset(self):
        # Владелец или модератор могут редактировать
        if self.request.user.groups.filter(name='Модератор продуктов').exists():
            return Product.objects.all()
        return Product.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        # Сбрасываем кеш списка опубликованных продуктов
        invalidate_published_products_cache()
        # Если изменили категорию — сбрасываем и кеш по категории
        old_category_id = self.get_object().category_id
        response = super().form_valid(form)
        if old_category_id != form.instance.category_id:
            invalidate_category_cache(old_category_id)
            invalidate_category_cache(form.instance.category_id)
        return response

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def get_queryset(self):
        # Владелец или модератор могут удалять
        if self.request.user.groups.filter(name='Модератор продуктов').exists():
            return Product.objects.all()
        return Product.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        #  Сбрасываем кеш списка опубликованных продуктов
        invalidate_published_products_cache()
        #  Сбрасываем кеш по категории
        product = self.get_object()
        invalidate_category_cache(product.category_id)
        return super().delete(request, *args, **kwargs)

class ProductUnpublishView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        old_category_id = product.category_id
        product.is_published = False
        product.save()
        # Сбрасываем кеш списка опубликованных продуктов
        invalidate_published_products_cache()
        # Сбрасываем кеш по категории
        invalidate_category_cache(old_category_id)
        return HttpResponseRedirect(reverse_lazy('catalog:product_detail', kwargs={'pk': pk}))

class ProductByCategoryView(ListView):
    model = Product
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        context['category'] = Category.objects.get(id=category_id)
        return context

# def product_detail(request, pk):
#     """Отображает страницу одного товара по его ID (pk)."""
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'catalog/product_detail.html', {'product': product})



# def home(request):
#     """Главная страница — список всех товаров."""
#     products = Product.objects.select_related('category').all()
#     return render(request, 'catalog/home.html', {'products': products})