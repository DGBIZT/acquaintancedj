from django.contrib import admin
from .models import Blog

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at','is_published',)
    list_filter = ('title','created_at','is_published',)
    search_fields = ('title','content','created_at', 'is_published',)
