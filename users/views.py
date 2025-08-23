from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.mail import send_mail
from .forms import CustomUserCreationForm, CustomAuthenticationForm


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        # Получаем объект пользователя
        user = form.save(commit=False)
        # Устанавливаем статус активности
        user.is_active = True
        # Сохраняем пользователя
        user.save()
        # Отправляем приветственное письмо
        self.send_welcome_email(user.email)
        # Автоматически авторизуем пользователя
        login(self.request, user)  # Логиним пользователя
        # return super().form_valid(form)
        return redirect(self.success_url)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш рынок онлайн'
        message = 'Спасибо что зарегистрировались на рынок онлайн'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email,]
        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            # Обработка
            print(f"Ошибка при отправке письма: {e}")

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:home')

    # обработка ошибок
    def form_invalid(self, form):
        print(form.errors)  # Для отладки
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        print(f"Пользователь {form.cleaned_data['username']} успешно вошел")
        return response



