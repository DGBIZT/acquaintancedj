from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('username','first_name', 'last_name', 'email')
    list_filter = ('username','first_name', 'last_name', 'email')
    search_fields = ('email',)

