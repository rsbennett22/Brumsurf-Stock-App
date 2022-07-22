from django.contrib import admin
from .models import StockItem, Wetsuit, Surfboard

class StockItemAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)

admin.site.register(StockItem, StockItemAdmin)
admin.site.register(Wetsuit, StockItemAdmin)
admin.site.register(Surfboard, StockItemAdmin)