from django.contrib import admin
from .models import StockItem, Wetsuit, Surfboard, Surfskate, Boot, Glove, Hood

class StockItemAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)

admin.site.register(StockItem, StockItemAdmin)
admin.site.register(Wetsuit, StockItemAdmin)
admin.site.register(Surfboard, StockItemAdmin)
admin.site.register(Surfskate, StockItemAdmin)
admin.site.register(Boot, StockItemAdmin)
admin.site.register(Glove, StockItemAdmin)
admin.site.register(Hood, StockItemAdmin)