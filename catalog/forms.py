from django import forms
from .models import Product, Category
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
        fields = ['title', 'description', 'image', 'purchase_price', 'category',]

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название товара'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Описание продукта'}),
            'purchase_price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }

        # help_texts = {
        #     'title': 'Не более 100 символов. Запрещены слова: казино, крипта, бесплатно и др.',
        #     'purchase_price': 'Стоимость закупки без скидок.',
        # }

    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        return price

            