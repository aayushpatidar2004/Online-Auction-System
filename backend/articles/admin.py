from django.contrib import admin
from .models import Article, GovernmentResource

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_government_scheme', 'published_date')
    list_filter = ('category', 'is_government_scheme')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(GovernmentResource)
class GovernmentResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'ministry_department', 'helpline')
    search_fields = ('name', 'ministry_department', 'description')

