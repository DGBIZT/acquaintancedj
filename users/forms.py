from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        # Сначала вызываем родительский конструктор без kwargs
        super().__init__(*args)

        # Обрабатываем request отдельно
        self.request = kwargs.pop('request', None)

        # Обновляем атрибуты полей
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите Email',
            'type': 'email',
            'autocomplete': 'email'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'autocomplete': 'current-password'
        })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Email обязателен для заполнения')
        return username


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20, required=False, help_text='Не обязательное поле. Введите Ваш номер телефона')
    username = forms.CharField(max_length=50, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'countries','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите Email'
        })

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите имя'
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите фамилию'
        })

        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите телефон'
        })

        self.fields['countries'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите страну'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль повторно'
        })

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            return forms.ValidationError('Номер телефона должен состоять только из цифр')
        return phone_number