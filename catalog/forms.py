from django import forms
from .models import Product


# Список запрещённых слов
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']


    def clean_name(self, word=None):
        name = self.cleaned_data['name']
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise forms.ValidationError(f"Название не должно содержать запрещённое слово: '{word}'")
        return name


    def clean_description(self, word=None):
        description = self.cleaned_data['description']
        if description:
            for word in FORBIDDEN_WORDS:
                if word.lower() in description.lower():
                    raise forms.ValidationError(f"Описание не должно содержать запрещённое слово: '{word}'")
        return description


    def clean_price(self, word=None):
        price = self.cleaned_data['price']
        if price is not None and price <= 0:
            raise forms.ValidationError("Цена не может быть отрицательной")
        return price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Применяем стили ко всем полям

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Опишите товар (без запрещённых слов: казино, крипта и т.д.)'
        })


        self.fields['image'].widget.attrs.update({
            'class': 'form-control'
        })


        self.fields['category'].widget.attrs.update({
            'class': 'form-select'
        })


        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01'
        })
