from django.contrib import admin
from .models import Pesticide

@admin.register(Pesticide)
class PesticideAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'active_ingredient', 'toxicity_label', 'pre_harvest_interval_days')
    list_filter = ('toxicity_label',)
    search_fields = ('product_name', 'active_ingredient', 'target_pests', 'target_crops')
