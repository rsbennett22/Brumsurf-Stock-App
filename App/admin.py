from django.contrib import admin
from .models import Wetsuit, StockItem

class StockItemAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)

admin.site.register(StockItem, StockItemAdmin)
admin.site.register(Wetsuit, StockItemAdmin)