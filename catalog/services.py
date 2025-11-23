from django.core.cache import cache
from .models import Product, Category

def get_products_by_category(category_id):
    """
    Возвращает список продуктов в указанной категории с кешированием
    """
    cache_key = f'products_by_category_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        products = list(Product.objects.filter(category_id=category_id, is_published=True))
        cache.set(cache_key, products, 60 * 15)

    return products

def get_published_products():
    """
    Возвращает список опубликованных продуктов с кешированием (для HomeView)
    """
    cache_key = 'published_products_list'
    products = cache.get(cache_key)

    if products is None:
        products = list(Product.objects.filter(is_published=True))
        cache.set(cache_key, products, 60 * 15)

    return products

def invalidate_published_products_cache():
    """
    Сбрасывает кеш списка опубликованных продуктов
    """
    cache.delete('published_products_list')

def invalidate_category_cache(category_id):
    """
    Сбрасывает кеш продуктов в указанной категории
    """
    cache_key = f'products_by_category_{category_id}'
    cache.delete(cache_key)
