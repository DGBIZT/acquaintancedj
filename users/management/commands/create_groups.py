from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')
        permissions = Permission.objects.filter(codename__in=['can_unpublish_product', 'delete_product', 'view_product', 'change_product', 'add_product', 'delete_blog', 'view_blog', 'change_blog', 'add_blog'])
        group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана с необходимыми правами.'))

