from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20, required=False, help_text='Не обязательное поле. Введите Ваш номер телефона')
    username = forms.CharField(max_length=50, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'countries','password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            return forms.ValidationError('Номер телефона должен состоять только из цифр')
        return phone_number