from django.core.management.base import  BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            username = 'moderator',
            email = 'moderator@sky.pro',
            first_name =  'Moderator',
            last_name = 'Moderator',
        )

        user.set_password('1234')

        user.is_staff = True
        user.is_superuser =False

        group = Group.objects.get(name='Модератор продуктов')
        user.groups.add(group)

        user.save()

        self.stdout.write(self.style.SUCCESS(f'Модератор успешно создан успешно создан {user.email}!'))