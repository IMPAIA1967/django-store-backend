from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми продуктами и категориями'

    def handle(self, *args, **options):
        # Удаляем все существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()


        # Создаем категории
        categories_data = [
            {'name': 'Электроника', 'description': 'Техника и гаджеты'},
            {'name': 'Книги', 'description': 'Художественная литература'},
            {'name': 'Одежда', 'description': 'Мужская и женская одежда'},
        ]

        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories[cat_data['name']] = category
            self.stdout.write(f'Создана категория: {category.name}')


        products_data = [
            {
                'name': 'iPhone 15',
                'description': 'Новый смартфон Apple',
                'category': categories['Электроника'],
                'price': 89999.99
            },
            {
                'name': 'MacBook Pro',
                'description': 'Ноутбук для работы',
                'category': categories['Электроника'],
                'price': 199999.99
            },
            {
                'name': 'Война и мир',
                'description': 'Роман Льва Толстого',
                'category': categories['Книги'],
                'price': 1500.00
            },
            {
                'name': 'Футболка',
                'description': 'Хлопковая футболка',
                'category': categories['Одежда'],
                'price': 1999.99
            },
        ]

        for prod_data in products_data:
            product = Product.objects.create(**prod_data)
            self.stdout.write(f'Создан продукт: {product.name} - {product.price} руб.')

