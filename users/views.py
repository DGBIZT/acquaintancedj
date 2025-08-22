from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.conf import settings
from django.core.mail import send_mail
from pyexpat.errors import messages

from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

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




