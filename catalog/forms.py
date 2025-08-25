from django import forms
from .models import Product
from django.core.exceptions import ValidationError

# Список запрещённых слов
FORBIDDEN_WORDS = {
    "казино", "криптовалюта", "крипта", "биржа",
    "дешево", "бесплатно", "обман", "полиция", "радар"
}
def validate_forbidden_words(value):
    """
    Проверяет, что текст не содержит запрещённых слов.
    """
    words = value.lower().split()
    cleaned_words = {word.strip(".,?!:;\"'()[]{}") for word in words}
    found = FORBIDDEN_WORDS.intersection(cleaned_words)
    if found:
        raise ValidationError(f"Недопустимые слова: {', '.join(found)}")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'purchase_price', 'category', 'is_published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder' : 'Введите название товара'
        })


        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Описание продукта'
        })

        self.fields['purchase_price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите цену'
        })

        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
        })



    def clean_title(self):
        title = self.cleaned_data.get('title')
        validate_forbidden_words(title)
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        validate_forbidden_words(description)
        return description

    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        return price

            