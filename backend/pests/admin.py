from django.contrib import admin
from .models import Pest

@admin.register(Pest)
class PestAdmin(admin.ModelAdmin):
    list_display = ('pest_name', 'scientific_name', 'affected_crops')
    search_fields = ('pest_name', 'affected_crops', 'symptoms')

